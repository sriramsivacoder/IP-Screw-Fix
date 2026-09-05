const IPR_LABELS = {
  patent: "Patent",
  trademark: "Trademark",
  design: "Design",
  copyright: "Copyright",
  trade_secret: "Trade Secret",
  geographical_indication: "Geographical Indication",
  plant_variety_protection: "Plant Variety Protection",
  traditional_knowledge: "Traditional Knowledge / Prior Art",
}

const RELEVANCE_BADGE = {
  potentially_relevant: "bg-ayush-bgblue text-ayush-darkgreen border-ayush-green/30",
  unclear: "bg-yellow-50 text-yellow-800 border-yellow-200",
  not_applicable: "bg-gray-50 text-gray-500 border-gray-200",
}

const RELEVANCE_LABELS = {
  potentially_relevant: "Potentially Relevant",
  unclear: "Unclear",
  not_applicable: "Not Applicable",
}

export default function IprRoutes({ iprRoutes }) {
  if (!iprRoutes || !iprRoutes.routes || iprRoutes.routes.length === 0) return null

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
      <p className="text-xs font-semibold text-ayush-green uppercase tracking-wider mb-1">
        Potentially Relevant IPR Routes
      </p>
      <p className="text-xs text-gray-500 mb-4">
        These routes are identified from the information provided. They are not legal conclusions.
      </p>

      <div className="space-y-2.5">
        {iprRoutes.routes.map((route, i) => {
          const iprLabel = IPR_LABELS[route.ipr] || route.ipr
          const badgeClass = RELEVANCE_BADGE[route.relevance] || RELEVANCE_BADGE.unclear
          const relevanceLabel = RELEVANCE_LABELS[route.relevance] || route.relevance

          return (
            <div
              key={i}
              className="border border-gray-100 rounded-lg px-4 py-3 bg-gray-50"
            >
              <div className="flex flex-wrap items-center gap-2 mb-1.5">
                <span className="text-sm font-semibold text-ayush-charcoal">
                  {iprLabel}
                </span>
                <span
                  className={`text-xs font-medium px-2 py-0.5 rounded border ${badgeClass}`}
                >
                  {relevanceLabel}
                </span>
              </div>
              <p className="text-xs text-gray-600 leading-relaxed">{route.reason}</p>
            </div>
          )
        })}
      </div>

      {iprRoutes.needs_human_review && (
        <div className="bg-ayush-bgred border border-red-200 text-red-800 text-xs px-3 py-2 rounded mt-4">
          Professional legal advice is recommended to assess the actual applicability of these routes to your specific situation.
        </div>
      )}
    </div>
  )
}
