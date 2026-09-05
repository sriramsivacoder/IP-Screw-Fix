export default function JurisdictionSwitch({ value, onChange, compact = false }) {
  const jurisdictions = ["India", "International"]

  if (compact) {
    return (
      <div className="flex gap-2" role="group" aria-label="Jurisdiction">
        {jurisdictions.map((j) => (
          <button
            key={j}
            type="button"
            onClick={() => onChange(j)}
            aria-pressed={value === j}
            className={`px-3 py-1 text-xs font-medium rounded border transition-colors ${
              value === j
                ? "bg-ayush-darkgreen text-white border-ayush-darkgreen"
                : "bg-white text-gray-600 border-gray-300 hover:border-ayush-green"
            }`}
          >
            {j}
          </button>
        ))}
      </div>
    )
  }

  return (
    <div className="flex flex-wrap gap-3" role="group" aria-label="Jurisdiction">
      {jurisdictions.map((j) => (
        <button
          key={j}
          type="button"
          onClick={() => onChange(j)}
          aria-pressed={value === j}
          className={`flex-1 sm:flex-none px-6 py-2.5 text-sm font-medium rounded border transition-colors ${
            value === j
              ? "bg-ayush-darkgreen text-white border-ayush-darkgreen"
              : "bg-white text-ayush-charcoal border-gray-300 hover:border-ayush-green hover:bg-ayush-bglight"
          }`}
        >
          {j}
        </button>
      ))}
    </div>
  )
}
