package com.mathan.aiapplication.data.repository

import com.mathan.aiapplication.data.remote.AiApi
import com.mathan.aiapplication.data.remote.AiRequest
import com.mathan.aiapplication.data.remote.AiResponse
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.flowOn
import javax.inject.Inject

class AiRepository @Inject constructor(
    private val api: AiApi
) {
    suspend fun askQuestion(question: String): AiResponse {
        return api.askQuestion(AiRequest(question))
    }

    fun askQuestionStream(question: String): Flow<String> = flow {
        val body = api.askQuestionStream(AiRequest(question))
        body.byteStream().bufferedReader().use { reader ->
            val buffer = CharArray(256)
            while (true) {
                val count = reader.read(buffer)
                if (count == -1) break
                if (count > 0) emit(String(buffer, 0, count))
            }
        }
    }.flowOn(Dispatchers.IO)
}