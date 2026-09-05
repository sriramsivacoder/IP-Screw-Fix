import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { classifyFormulation } from "../services/api"

const ALL_QUESTIONS = [
  {
    id: "intended_use",
    text: "What is the intended use of this formulation?",
    options: [
      { value: "medicine", label: "Medicine" },
      { value: "food_nutraceutical", label: "Food or Nutraceutical" },
      { value: "cosmetic", label: "Cosmetic" },
      { value: "other", label: "Other" },
      { value: "not_sure", label: "Not sure" },
    ],
    showIf: null,
  },
  {
    id: "classical_source",
    text: "Is this medicine based on an authoritative classical Ayurvedic text or formulary (such as the Ayurvedic Pharmacopoeia of India or Ayurvedic Formulary of India)?",
    options: [
      { value: "yes", label: "Yes" },
      { value: "no", label: "No" },
      { value: "not_sure", label: "Not sure" },
    ],
    showIf: { field: "intended_use", value: "medicine" },
  },
  {
    id: "substantially_modified",
    text: "Has the formulation been substantially modified or is it a new formulation not found in classical Ayurvedic texts?",
    options: [
      { value: "yes", label: "Yes" },
      { value: "no", label: "No" },
      { value: "not_sure", label: "Not sure" },
    ],
    showIf: null,
  },
  {
    id: "new_process",
    text: "Is there a new or novel manufacturing process involved in producing this formulation?",
    options: [
      { value: "yes", label: "Yes" },
      { value: "no", label: "No" },
      { value: "not_sure", label: "Not sure" },
    ],
    showIf: null,
  },
  {
    id: "geographical_association",
    text: "Does the product have a geographical association or a reputation linked to a specific region or geographical area?",
    options: [
      { value: "yes", label: "Yes" },
      { value: "no", label: "No" },
      { value: "not_sure", label: "Not sure" },
    ],
    showIf: null,
  },
  {
    id: "biological_resources_from_india",
    text: "Were the biological resources used in this formulation obtained from India?",
    options: [
      { value: "yes", label: "Yes" },
      { value: "no", label: "No" },
      { value: "not_sure", label: "Not sure" },
    ],
    showIf: null,
  },
]

function getActiveQuestions(answers) {
  return ALL_QUESTIONS.filter((q) => {
    if (!q.showIf) return true
    return answers[q.showIf.field] === q.showIf.value
  })
}

export default function FormulationPage({ answers, setAnswers, onDone }) {
  const [currentStep, setCurrentStep] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [slideDirection, setSlideDirection] = useState(1)

  const activeQuestions = getActiveQuestions(answers)
  const question = activeQuestions[currentStep]
  const totalSteps = activeQuestions.length
  const isLastStep = currentStep === totalSteps - 1
  const currentAnswer = question ? answers[question.id] : undefined

  function handleOptionClick(value) {
    if (!question) return

    const updatedAnswers = { ...answers, [question.id]: value }
    setAnswers(updatedAnswers)

    const updatedActive = getActiveQuestions(updatedAnswers)
    if (currentStep < updatedActive.length - 1) {
      setSlideDirection(1)
      setCurrentStep(currentStep + 1)
    }
  }

  function handleBack() {
    if (currentStep > 0) {
      setSlideDirection(-1)
      setCurrentStep(currentStep - 1)
    }
  }

  async function handleSubmit() {
    setLoading(true)
    setError(null)
    try {
      const result = await classifyFormulation(answers)
      onDone(result.classification, result.ipr_routes)
    } catch (err) {
      setError(
        err.message ||
          "Classification failed. Please check that the backend server is running."
      )
    } finally {
      setLoading(false)
    }
  }

  if (!question) return null

  return (
    <div>
      <div className="mb-7">
        <h2 className="text-xl font-semibold text-ayush-charcoal mb-1.5">
          Formulation Details
        </h2>
        <p className="text-sm text-gray-500">
          Answer the following questions about your formulation. You can go back and change any answer at any time.
        </p>
      </div>

      <div className="flex items-center gap-1.5 mb-2">
        {activeQuestions.map((_, i) => (
          <div
            key={i}
            className={`h-1 flex-1 rounded-full transition-colors duration-300 ${
              i < currentStep
                ? "bg-ayush-green"
                : i === currentStep
                ? "bg-ayush-darkgreen"
                : "bg-gray-200"
            }`}
          />
        ))}
      </div>
      <p className="text-xs text-gray-400 mb-6">
        Question {currentStep + 1} of {totalSteps}
      </p>

      <AnimatePresence mode="wait" initial={false}>
        <motion.div
          key={question.id}
          initial={{ opacity: 0, x: slideDirection * 24 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: slideDirection * -24 }}
          transition={{ duration: 0.18, ease: "easeInOut" }}
        >
          <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm mb-6">
            <p className="text-ayush-charcoal font-medium text-sm sm:text-base leading-relaxed mb-5">
              {question.text}
            </p>

            <div className="flex flex-col gap-2.5">
              {question.options.map((option) => (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => handleOptionClick(option.value)}
                  className={`w-full text-left px-4 py-3 rounded border text-sm font-medium transition-all ${
                    currentAnswer === option.value
                      ? "bg-ayush-darkgreen text-white border-ayush-darkgreen"
                      : "bg-white text-ayush-charcoal border-gray-200 hover:border-ayush-green hover:bg-ayush-bglight"
                  }`}
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>
        </motion.div>
      </AnimatePresence>

      {error && (
        <div className="bg-ayush-bgred border border-red-200 text-red-800 text-sm px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <div className="flex items-center justify-between gap-3">
        <button
          type="button"
          onClick={handleBack}
          disabled={currentStep === 0}
          className="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          Back
        </button>

        {isLastStep && currentAnswer !== undefined && (
          <button
            type="button"
            onClick={handleSubmit}
            disabled={loading}
            className="px-6 py-2 text-sm font-medium bg-ayush-darkgreen text-white rounded hover:bg-ayush-green disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? "Classifying…" : "Classify Formulation"}
          </button>
        )}
      </div>
    </div>
  )
}
