package com.mathan.aiapplication.redux.ai

import com.mathan.aiapplication.redux.Action

sealed class AiAction : Action {
    data class AskQuestion(val question: String) : AiAction()
    data class AnswerToken(val token: String) : AiAction()
    object StreamCompleted : AiAction()

    open class ClearAnswer : AiAction()
    data class Error(val message: String) : AiAction()
}
