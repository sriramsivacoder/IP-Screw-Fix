const CATEGORY_LABELS = {
  classical_medicine: "Classical Medicine",
  proprietary_or_modified_medicine: "Proprietary or Modified Medicine",
  new_or_non_classical_medicine: "New or Non-Classical Medicine",
  food_nutraceutical: "Food or Nutraceutical",
  cosmetic: "Cosmetic",
  unknown: "Undetermined",
}

const CONFIDENCE_BADGE = {
  high: "bg-green-50 text-green-800 border-green-200",
  medium: "bg-yellow-50 text-yellow-800 border-yellow-200",
  low: "bg-red-50 text-red-800 border-red-200",
}

export default function ClassificationCard({ classification }) {
  if (!classification) return null

  const { category, confidence, reason, needs_human_review } = classification
  const categoryLabel = CATEGORY_LABELS[category] || category
  const badgeClass = CONFIDENCE_BADGE[confidence] || CONFIDENCE_BADGE.low
  const confidenceLabel =
    confidence.charAt(0).toUpperCase() + confidence.slice(1) + " Confidence"

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
      <p className="text-xs font-semibold text-ayush-green uppercase tracking-wider mb-3">
        Likely Formulation Category
      </p>

      <div className="flex flex-wrap items-center gap-3 mb-4">
        <span className="text-lg font-semibold text-ayush-charcoal">
          {categoryLabel}
        </span>
        <span
          className={`text-xs font-medium px-2 py-0.5 rounded border ${badgeClass}`}
        >
          {confidenceLabel}
        </span>
      </div>

      {reason && reason.length > 0 && (
        <ul className="space-y-1.5 mb-4">
          {reason.map((r, i) => (
            <li key={i} className="flex gap-2 text-sm text-gray-600">
              <span className="text-ayush-green mt-0.5 shrink-0 font-medium">›</span>
              <span>{r}</span>
            </li>
          ))}
        </ul>
      )}

      {needs_human_review && (
        <div className="bg-ayush-bgred border border-red-200 text-red-800 text-xs px-3 py-2 rounded">
          Human and legal review is recommended before drawing any conclusions from this classification.
        </div>
      )}

      <p className="text-xs text-gray-400 mt-4 leading-relaxed">
        This is a potential classification for informational purposes only and does not constitute a legal or regulatory determination.
      </p>
    </div>
  )
}
