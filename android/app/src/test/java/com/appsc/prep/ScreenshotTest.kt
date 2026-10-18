package com.appsc.prep

import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.ui.test.assertCountEquals
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onAllNodesWithContentDescription
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.onRoot
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollToNode
import androidx.test.core.app.ApplicationProvider
import com.appsc.prep.data.ProgressStore
import com.appsc.prep.data.Question
import com.appsc.prep.data.Repository
import com.appsc.prep.data.TableBlock
import com.appsc.prep.platform.AndroidPlatform
import com.appsc.prep.platform.PrefsStorage
import com.appsc.prep.platform.ReadAloud
import com.appsc.prep.ui.components.AppState
import com.appsc.prep.ui.components.LocalApp
import com.appsc.prep.ui.components.SpeechPage
import com.appsc.prep.ui.screens.BooksScreen
import com.appsc.prep.ui.screens.DayScreen
import com.appsc.prep.ui.screens.Nav
import com.appsc.prep.ui.screens.PlanScreen
import com.appsc.prep.ui.screens.ProgressScreen
import com.appsc.prep.ui.screens.QuizRound
import com.appsc.prep.ui.screens.ReaderScreen
import com.appsc.prep.ui.screens.SectionScreen
import com.appsc.prep.ui.screens.TodayScreen
import com.appsc.prep.ui.theme.PrepTheme
import com.github.takahirom.roborazzi.captureRoboImage
import kotlinx.coroutines.runBlocking
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode

/**
 * CA Prep screens drawn on the JVM (./gradlew recordRoborazziDebug -> app/screenshots/). The notes are whatever
 * scripts/build_ca_assets.py wrote, so the tests pick their pages from the assets instead of fixed titles.
 */
@RunWith(RobolectricTestRunner::class)
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@Config(sdk = [34], qualifiers = "w400dp-h860dp-xxhdpi")
class ScreenshotTest {
    @get:Rule
    val rule = createComposeRule()

    private val nav = object : Nav {
        override fun quiz(kind: String, book: Int, index: Int, mode: String, sub: Int) {}
        override fun day(n: Int) {}
        override fun row(book: Int, row: Int) {}
        override fun read(book: Int, row: Int, sec: Int) {}
        override fun book(id: Int) {}
        override fun back() {}
    }

    private val ctx get() = ApplicationProvider.getApplicationContext<android.content.Context>()
    private val repo by lazy { Repository { ctx.assets.open(it) } }
    private val firstBook get() = repo.index.first().id

    private fun shot(name: String, preload: Int? = null, content: @Composable () -> Unit) {
        ReadAloud.init(ctx).stop() // each screen starts without read-aloud
        val app = AppState(Repository { ctx.assets.open(it) }, ProgressStore(PrefsStorage(ctx)), AndroidPlatform(ctx))
        if (preload != null) runBlocking { app.repo.book(preload); app.repo.mcq(preload) }
        rule.setContent {
            PrepTheme { CompositionLocalProvider(LocalApp provides app) { content() } }
        }
        rule.waitForIdle()
        rule.onRoot().captureRoboImage("screenshots/$name.png")
    }

    @Test fun today() = shot("1_today") { TodayScreen(nav) }
    @Test fun plan() = shot("2_plan") { PlanScreen(nav) }
    @Test fun day1() = shot("3_day1") { DayScreen(1, nav) }

    @Test fun weeklyReview() {
        val n = repo.plan.days.first { it.type == "sunday" }.n
        shot("3b_weekly_review") { DayScreen(n, nav) }
    }

    @Test fun books() {
        shot("7_notes") { BooksScreen(nav) }
        rule.onNodeWithText(repo.index.first().title).assertExists()
    }

    /** A topic (category file) of the newest month: its pages, and MCQ practice exactly when it has questions. */
    @Test fun section() {
        val app = AppState(Repository { ctx.assets.open(it) }, ProgressStore(PrefsStorage(ctx)), AndroidPlatform(ctx))
        runBlocking { app.repo.book(firstBook); app.repo.mcq(firstBook) }
        rule.mainClock.autoAdvance = false
        rule.setContent { PrepTheme { CompositionLocalProvider(LocalApp provides app) { SectionScreen(firstBook, 0, nav) } } }
        rule.mainClock.advanceTimeBy(3000)
        rule.onNodeWithText(repo.index.first().rows[0].title).assertExists()
        if (repo.index.first().rows[0].questionCount > 0) rule.onAllNodesWithText("Practice", substring = true)[0].assertExists()
        else rule.onAllNodesWithText("Practice", substring = true).assertCountEquals(0)
        rule.onRoot().captureRoboImage("screenshots/4_section.png")
        rule.mainClock.autoAdvance = true
    }

    @Test fun reader() {
        shot("5_reader", preload = firstBook) { ReaderScreen(firstBook, 0, 0, nav) }
        rule.onAllNodesWithText("Sources: ", substring = true)[0].assertExists()
        rule.onAllNodesWithText("Practice", substring = true).assertCountEquals(0)
    }

    /** The first page with a table. */
    @Test fun readerTable() {
        val book = runBlocking { repo.book(firstBook) }
        val (r, s) = book.rows.flatMap { row -> row.secs.indices.map { row.index to it } }
            .first { (r, s) -> book.rows[r].secs[s].blocks.take(4).any { it is TableBlock } }
        shot("6_reader_table", preload = firstBook) { ReaderScreen(firstBook, r, s, nav) }
    }

    /** Read aloud: the Listen button opens the player bar and speaks the page. */
    @Test fun readerListen() {
        shot("15_listen", preload = firstBook) { ReaderScreen(firstBook, 0, 0, nav) }
        rule.onNodeWithContentDescription("Listen").performClick()
        rule.waitForIdle()
        org.robolectric.shadows.ShadowLooper.idleMainLooper()
        rule.waitForIdle()
        rule.onNodeWithContentDescription("Pause").assertExists()
        rule.onRoot().captureRoboImage("screenshots/15_listen.png")
        assertEquals("$firstBook:0:0", ReadAloud.playback.value.pageId)
        assertTrue(ReadAloud.playback.value.playing)
        ReadAloud.stop()
    }

    /** Google's copy menu does not show inside the app, so the page's paragraphs are listed to tick. */
    @Test fun pickTextFromGoogle() {
        var added = ""
        val paras = listOf("Amaravati Quantum Valley", "IBM Quantum System Two", "156-qubit Heron processor")
        shot("25_pick_text") { com.appsc.prep.ui.components.PickText(paras, preselect = 0, onAdd = { added = it }) {} }
        rule.onNodeWithText(paras[2]).performClick()
        rule.onNodeWithText("Add (2)").performClick()
        assertEquals(paras[0] + "\n" + paras[2], added)
    }

    /** ⋮ → Explain simply. */
    @Test fun explainSimply() {
        shot("28_explain_menu", preload = firstBook) { ReaderScreen(firstBook, 0, 0, nav) }
        rule.onNodeWithContentDescription("More").performClick()
        rule.waitForIdle()
        rule.onNodeWithText("Explain simply").assertExists()
        val p = com.appsc.prep.ui.screens.simplePrompt("Quantum Valley", "Quantum Valley\n• IBM Quantum System Two [GK] (CDI).\n")
        assertTrue(p, p.startsWith("Explain this in very simple English, as if to a class 6 student."))
        assertTrue(com.appsc.prep.ui.components.googleAiUrl("a b").startsWith("https://www.google.com/search?udm=50&"))
    }

    /** A page's key terms at its end; tapping one opens its meaning. */
    @Test fun keyTermsOnAPage() {
        val key = repo.keyTerms.keys.first { it.startsWith("$firstBook:") }
        val (b, r, s) = key.split(':').map { it.toInt() }
        shot("17_key_terms", preload = b) { ReaderScreen(b, r, s, nav) }
        rule.onNode(androidx.compose.ui.test.hasScrollToNodeAction()).performScrollToNode(androidx.compose.ui.test.hasText("KEY TERMS"))
        rule.waitForIdle()
        rule.onRoot().captureRoboImage("screenshots/17_key_terms.png")
        rule.onAllNodesWithText(repo.keyTerms.getValue(key).first())[0].performClick()
        rule.waitUntil(20_000) { rule.onAllNodesWithText("MEANING").fetchSemanticsNodes().isNotEmpty() || rule.onAllNodesWithText("IN INDIAN CONTEXT").fetchSemanticsNodes().isNotEmpty() }
        rule.onRoot().captureRoboImage("screenshots/18_key_term_meaning.png")
        rule.onAllNodesWithContentDescription("Close").fetchSemanticsNodes().let { if (it.isNotEmpty()) rule.onAllNodesWithContentDescription("Close")[0].performClick() }
    }

    /** Reading page A, then opening page B by hand: B is read. */
    @Test fun readAloudFollowsTheOpenedPage() {
        ReadAloud.init(ctx).play(SpeechPage("$firstBook:1:0", "A", listOf("one", "two")), 0, 1f) { null }
        val app = AppState(Repository { ctx.assets.open(it) }, ProgressStore(PrefsStorage(ctx)), AndroidPlatform(ctx))
        runBlocking { app.repo.book(firstBook); app.repo.mcq(firstBook) }
        rule.setContent { PrepTheme { CompositionLocalProvider(LocalApp provides app) { ReaderScreen(firstBook, 0, 0, nav) } } }
        rule.waitForIdle()
        assertEquals("$firstBook:0:0", ReadAloud.playback.value.pageId)
        ReadAloud.stop()
    }

    /** MCQ practice still works for when questions are added (a made-up question, no assets needed). */
    @Test fun quizRound() {
        val q = Question(
            id = "t1", stem = "Which district has the Ramayapatnam port?", table = emptyList(),
            options = listOf("Prakasam", "Srikakulam", "Krishna", "Kakinada"), answer = 0, source = "", appsc = false,
            explanation = "Ramayapatnam is a state port in Prakasam district.", notes = emptyList(), book = firstBook,
        )
        shot("9_quiz") { QuizRound("t", listOf(q), listOf(q), {}, {}) }
        rule.onNodeWithText("Prakasam").performClick()
        rule.waitForIdle()
        rule.onRoot().captureRoboImage("screenshots/10_quiz_answered.png")
    }

    @Test fun progress() {
        shot("8_progress") { ProgressScreen(nav) }
        rule.onNode(androidx.compose.ui.test.hasScrollToNodeAction()).performScrollToNode(androidx.compose.ui.test.hasText("Back up now"))
        rule.waitForIdle()
        rule.onAllNodesWithText("Last backup: never").fetchSemanticsNodes().let { assertEquals(1, it.size) }
        rule.onRoot().captureRoboImage("screenshots/26_backup.png")
    }
}
