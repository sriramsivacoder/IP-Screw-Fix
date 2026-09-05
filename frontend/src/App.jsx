import { useState } from "react"
import StepIndicator from "./components/StepIndicator"
import Disclaimer from "./components/Disclaimer"
import FormulationPage from "./pages/FormulationPage"
import ClassifyResultPage from "./pages/ClassifyResultPage"
import ChatPage from "./pages/ChatPage"
import "./App.css"

export default function App() {
  const [stage, setStage] = useState("formulation")
  const [answers, setAnswers] = useState({})
  const [classification, setClassification] = useState(null)
  const [iprRoutes, setIprRoutes] = useState(null)
  const [jurisdiction, setJurisdiction] = useState("India")

  function handleClassifyDone(classificationResult, iprRoutesResult) {
    setClassification(classificationResult)
    setIprRoutes(iprRoutesResult)
    setStage("classify")
  }

  function handleRestart() {
    setStage("formulation")
    setAnswers({})
    setClassification(null)
    setIprRoutes(null)
    setJurisdiction("India")
  }

  return (
    <div className="min-h-screen bg-ayush-bglight flex flex-col">
      <header className="bg-ayush-darkgreen text-white px-4 py-4 shadow-sm">
        <div className="max-w-3xl mx-auto flex items-center justify-between">
          <div>
            <span className="text-base font-semibold tracking-tight block leading-tight">
              Ayurveda IPR Assistant
            </span>
            <span className="text-xs text-emerald-300 mt-0.5 block">
              Smart India Hackathon &middot; Phase 2
            </span>
          </div>
          {stage !== "formulation" && (
            <button
              type="button"
              onClick={handleRestart}
              className="text-xs text-emerald-300 hover:text-white border border-emerald-700 hover:border-white px-3 py-1.5 rounded transition-colors"
            >
              Start Over
            </button>
          )}
        </div>
      </header>

      <main className="flex-1 max-w-3xl mx-auto w-full px-4 py-8">
        <StepIndicator stage={stage} />

        {stage === "formulation" && (
          <FormulationPage
            answers={answers}
            setAnswers={setAnswers}
            onDone={handleClassifyDone}
          />
        )}

        {stage === "classify" && (
          <ClassifyResultPage
            classification={classification}
            iprRoutes={iprRoutes}
            jurisdiction={jurisdiction}
            setJurisdiction={setJurisdiction}
            onProceed={() => setStage("chat")}
            onBack={() => setStage("formulation")}
          />
        )}

        {stage === "chat" && (
          <ChatPage
            classification={classification}
            iprRoutes={iprRoutes}
            jurisdiction={jurisdiction}
            onBack={() => setStage("classify")}
          />
        )}
      </main>

      <Disclaimer />
    </div>
  )
}
