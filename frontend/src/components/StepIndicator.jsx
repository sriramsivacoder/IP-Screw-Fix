const STEPS = [
  { id: "formulation", label: "Formulation" },
  { id: "classify", label: "Classification" },
  { id: "chat", label: "Ask Question" },
]

export default function StepIndicator({ stage }) {
  const currentIndex = STEPS.findIndex((s) => s.id === stage)

  return (
    <div className="flex items-start mb-8">
      {STEPS.map((step, i) => {
        const isComplete = i < currentIndex
        const isCurrent = i === currentIndex

        return (
          <div key={step.id} className="flex items-center flex-1">
            <div className="flex flex-col items-center min-w-0">
              <div
                className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-semibold border-2 shrink-0 ${
                  isComplete
                    ? "bg-ayush-green border-ayush-green text-white"
                    : isCurrent
                    ? "bg-ayush-darkgreen border-ayush-darkgreen text-white"
                    : "bg-white border-gray-300 text-gray-400"
                }`}
              >
                {isComplete ? "✓" : i + 1}
              </div>
              <span
                className={`text-xs mt-1.5 font-medium text-center leading-tight ${
                  isCurrent
                    ? "text-ayush-darkgreen"
                    : isComplete
                    ? "text-ayush-green"
                    : "text-gray-400"
                }`}
              >
                {step.label}
              </span>
            </div>
            {i < STEPS.length - 1 && (
              <div
                className={`flex-1 h-px mx-2 mb-5 ${
                  i < currentIndex ? "bg-ayush-green" : "bg-gray-200"
                }`}
              />
            )}
          </div>
        )
      })}
    </div>
  )
}
