package com.mathan.aiapplication.redux.ai

import com.mathan.aiapplication.data.repository.AiRepository
import com.mathan.aiapplication.redux.Action
import com.mathan.aiapplication.redux.Middleware
import com.mathan.aiapplication.redux.Store

class AiMiddleware(private val repository: AiRepository) : Middleware<AiState> {
    override suspend fun process(state: AiState, action: Action, store: Store<AiState>) {
        when (action) {
            is AiAction.AskQuestion -> {
                try {
                    repository.askQuestionStream(action.question).collect { token ->
                        store.dispatch(AiAction.AnswerToken(token))
                    }
                    store.dispatch(AiAction.StreamCompleted)
                } catch (e: Exception) {
                    store.dispatch(AiAction.Error(e.message ?: "Unknown Error"))
                }
            }
        }
    }
}
