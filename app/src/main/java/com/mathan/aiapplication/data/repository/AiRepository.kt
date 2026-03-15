package com.mathan.aiapplication.data.repository

import com.mathan.aiapplication.data.remote.AiApi
import com.mathan.aiapplication.data.remote.AiRequest
import com.mathan.aiapplication.data.remote.AiResponse
import javax.inject.Inject

class AiRepository @Inject constructor(
    private val api: AiApi
) {
    suspend fun askQuestion(question: String): AiResponse {
        return api.askQuestion(AiRequest(question))
    }
}
