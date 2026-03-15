package com.mathan.aiapplication.viewmodel

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.mathan.aiapplication.data.repository.AiRepository
import com.mathan.aiapplication.redux.*
import com.mathan.aiapplication.redux.ai.AiAction
import com.mathan.aiapplication.redux.ai.AiMiddleware
import com.mathan.aiapplication.redux.ai.AiState
import com.mathan.aiapplication.redux.ai.reducer
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class AiViewModel @Inject constructor(
    private val repository: AiRepository
) : ViewModel() {
    
    private val middleware = AiMiddleware(repository)
    private val store = Store(
        initialState = AiState(),
        reducer = reducer,
        middlewares = listOf(middleware)
    )

    val state: StateFlow<AiState> = store.state

    fun dispatch(action: AiAction) {
        viewModelScope.launch(Dispatchers.IO) {
            Log.d("AiViewModel", "Current thread: ${Thread.currentThread().name}")
            store.dispatch(action)
        }
    }

    fun askQuestion(question: String) {
        dispatch(AiAction.AskQuestion(question))
    }
}
