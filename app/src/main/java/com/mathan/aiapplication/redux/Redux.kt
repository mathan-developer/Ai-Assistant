package com.mathan.aiapplication.redux

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

interface State

interface Action

typealias Reducer<S> = (S, Action) -> S

interface Middleware<S : State> {
    suspend fun process(state: S, action: Action, store: Store<S>)
}

class Store<S : State>(
    initialState: S,
    private val reducer: Reducer<S>,
    private val middlewares: List<Middleware<S>> = emptyList()
) {
    private val _state = MutableStateFlow(initialState)
    val state: StateFlow<S> = _state.asStateFlow()

    suspend fun dispatch(action: Action) {
        val currentState = _state.value
        val newState = reducer(currentState, action)
        _state.value = newState
        
        middlewares.forEach { it.process(newState, action, this) }
    }
}
