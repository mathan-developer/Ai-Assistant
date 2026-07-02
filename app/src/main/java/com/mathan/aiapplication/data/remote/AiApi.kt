package com.mathan.aiapplication.data.remote

import okhttp3.ResponseBody
import retrofit2.http.Body
import retrofit2.http.POST
import retrofit2.http.Streaming

interface AiApi {
    @POST("ask")
    suspend fun askQuestion(@Body request: AiRequest): AiResponse

    @Streaming
    @POST("ask/stream")
    suspend fun askQuestionStream(@Body request: AiRequest): ResponseBody
}

data class AiRequest(val question: String)
data class AiResponse(val answer: String)
