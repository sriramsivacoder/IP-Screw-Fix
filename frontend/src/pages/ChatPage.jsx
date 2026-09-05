import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { sendChatMessage } from "../services/api"
import JurisdictionSwitch from "../components/JurisdictionSwitch"
import SourceList from "../components/SourceList"

export default function ChatPage({ classification, iprRoutes, jurisdiction, onBack }) {
  const [currentJurisdiction, setCurrentJurisdiction] = useState(jurisdiction)
  const [question, setQuestion] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()

    const trimmed = question.trim()
    if (!trimmed || trimmed.length < 3) {
      setError("Please enter a question of at least 3 characters.")
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await sendChatMessage(
        trimmed,
        currentJurisdiction,
        classification,
        iprRoutes
      )
      setResult(response)
    } catch (err) {
      setError(
        err.message ||
          "Request failed. Please check that the backend server and Ollama are running."
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="flex items-start justify-between gap-4 mb-7">
        <div>
          <h2 className="text-xl font-semibold text-ayush-charcoal mb-1.5">
            Ask a Question
          </h2>
          <p className="text-sm text-gray-500">
            Ask a question about intellectual property for your formulation. Answers are
            grounded in retrieved authoritative legal documents.
          </p>
        </div>
        <button
          type="button"
          onClick={onBack}
          className="shrink-0 text-xs text-gray-500 hover:text-gray-700 border border-gray-300 px-3 py-1.5 rounded transition-colors"
        >
          Back
        </button>
      </div>

      <div className="bg-white border border-gray-200 rounded-lg px-4 py-3 mb-5 shadow-sm flex flex-wrap items-center gap-3">
        <span className="text-xs text-gray-500 font-medium">Jurisdiction:</span>
        <JurisdictionSwitch
          value={currentJurisdiction}
          onChange={setCurrentJurisdiction}
          compact
        />
        <span className="text-xs text-gray-400 ml-auto hidden sm:block">
          Retrieval is limited to {currentJurisdiction} sources.
        </span>
      </div>

      <form onSubmit={handleSubmit} className="mb-6">
        <label
          htmlFor="chat-question"
          className="block text-sm font-medium text-ayush-charcoal mb-2"
        >
          Your Question
        </label>
        <textarea
          id="chat-question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. What does Section 3(p) of the Patents Act say about traditional knowledge?"
          rows={3}
          className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm text-ayush-charcoal placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-ayush-darkgreen focus:border-ayush-darkgreen resize-none"
        />
        <div className="flex items-center justify-between mt-3">
          <span className="text-xs text-gray-400">
            {question.trim().length}/2000
          </span>
          <button
            type="submit"
            disabled={loading || question.trim().length < 3}
            className="px-6 py-2 text-sm font-medium bg-ayush-darkgreen text-white rounded hover:bg-ayush-green disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? "Searching…" : "Get Answer"}
          </button>
        </div>
      </form>

      {error && (
        <div className="bg-ayush-bgred border border-red-200 text-red-800 text-sm px-4 py-3 rounded mb-5">
          {error}
        </div>
      )}

      {loading && (
        <div className="flex items-center gap-3 text-sm text-gray-500 mb-5">
          <div className="w-4 h-4 border-2 border-ayush-green border-t-transparent rounded-full animate-spin" />
          Retrieving sources and generating answer…
        </div>
      )}

      <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25 }}
            className="space-y-5"
          >
            <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
              <div className="flex items-start justify-between gap-3 mb-4">
                <p className="text-xs font-semibold text-ayush-green uppercase tracking-wider">
                  Answer
                </p>
                <span className="shrink-0 text-xs bg-ayush-bgblue text-ayush-darkgreen border border-ayush-green/30 px-2 py-0.5 rounded font-medium">
                  {result.jurisdiction}
                </span>
              </div>

              {result.needs_human_review && (
                <div className="bg-ayush-bgred border border-red-200 text-red-800 text-xs px-3 py-2 rounded mb-4">
                  Human and legal review is recommended for this matter.
                </div>
              )}

              <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
                {result.answer}
              </p>
            </div>

            <SourceList sources={result.sources} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
