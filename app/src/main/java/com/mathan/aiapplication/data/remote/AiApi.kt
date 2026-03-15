package com.mathan.aiapplication.data.remote

import retrofit2.http.Body
import retrofit2.http.POST

interface AiApi {
    @POST("ask")
    suspend fun askQuestion(@Body request: AiRequest): AiResponse
}

data class AiRequest(val question: String)
data class AiResponse(val answer: String)
