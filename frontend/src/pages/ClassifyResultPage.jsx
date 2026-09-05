import { motion } from "framer-motion"
import ClassificationCard from "../components/ClassificationCard"
import IprRoutes from "../components/IprRoutes"
import JurisdictionSwitch from "../components/JurisdictionSwitch"

export default function ClassifyResultPage({
  classification,
  iprRoutes,
  jurisdiction,
  setJurisdiction,
  onProceed,
  onBack,
}) {
  return (
    <div>
      <div className="mb-7">
        <h2 className="text-xl font-semibold text-ayush-charcoal mb-1.5">
          Classification &amp; Potential IPR Routes
        </h2>
        <p className="text-sm text-gray-500">
          Based on your answers, the system has identified a likely formulation category and
          potentially relevant intellectual property routes. These results are informational
          only and do not constitute legal determinations.
        </p>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.25 }}
        className="space-y-5"
      >
        <ClassificationCard classification={classification} />
        <IprRoutes iprRoutes={iprRoutes} />

        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <p className="text-xs font-semibold text-ayush-green uppercase tracking-wider mb-1">
            Jurisdiction
          </p>
          <p className="text-sm text-gray-500 mb-4">
            Select the jurisdiction for which you want to retrieve legal information. India and
            International sources are kept separate to avoid mixing different legal frameworks.
          </p>
          <JurisdictionSwitch value={jurisdiction} onChange={setJurisdiction} />
        </div>

        <div className="flex flex-wrap gap-3 pt-1">
          <button
            type="button"
            onClick={onBack}
            className="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded hover:bg-gray-50 transition-colors"
          >
            Back to Formulation
          </button>
          <button
            type="button"
            onClick={onProceed}
            className="px-6 py-2 text-sm font-medium bg-ayush-darkgreen text-white rounded hover:bg-ayush-green transition-colors"
          >
            Proceed to Ask a Question
          </button>
        </div>
      </motion.div>
    </div>
  )
}
