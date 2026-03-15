package com.mathan.aiapplication.redux.ai

import com.mathan.aiapplication.redux.Reducer
import com.mathan.aiapplication.redux.State

data class AiState(
    val answer: String = "",
    val isLoading: Boolean = false,
    val error: String? = null
) : State

val reducer: Reducer<AiState> = { state, action ->
    when (action) {
        is AiAction.AskQuestion -> state.copy(isLoading = true, error = null, answer = "")
        is AiAction.AnswerReceived -> state.copy(isLoading = false, answer = action.answer)
        is AiAction.Error -> state.copy(isLoading = false, error = action.message)
        is AiAction.ClearAnswer -> state.copy(answer = "")
        else -> state
    }
}
