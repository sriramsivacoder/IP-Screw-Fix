import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"

function SourceItem({ source, index }) {
  const [expanded, setExpanded] = useState(index === 0)

  const metaFields = [
    { label: "Authority", value: source.authority },
    { label: "Jurisdiction", value: source.jurisdiction },
    { label: "Page", value: source.page },
    { label: "Section", value: source.section },
    { label: "Article", value: source.article },
    { label: "Effective Date", value: source.effective_date },
  ].filter((f) => f.value)

  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden">
      <button
        type="button"
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between px-4 py-3 bg-gray-50 hover:bg-gray-100 transition-colors text-left gap-3"
        aria-expanded={expanded}
      >
        <div className="flex items-center gap-3 min-w-0">
          <span className="shrink-0 text-xs font-semibold text-ayush-darkgreen bg-ayush-bglight border border-ayush-green/30 px-2 py-0.5 rounded">
            Source {index + 1}
          </span>
          <span className="text-sm font-medium text-ayush-charcoal truncate">
            {source.document}
          </span>
        </div>
        <span className="text-gray-400 shrink-0 text-base leading-none">
          {expanded ? "−" : "+"}
        </span>
      </button>

      <AnimatePresence initial={false}>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.18, ease: "easeInOut" }}
            className="overflow-hidden"
          >
            <div className="px-4 py-3 bg-white border-t border-gray-100">
              {metaFields.length > 0 && (
                <dl className="grid grid-cols-2 sm:grid-cols-3 gap-x-6 gap-y-1.5 mb-3">
                  {metaFields.map((f) => (
                    <div key={f.label}>
                      <dt className="text-xs text-gray-400">{f.label}</dt>
                      <dd className="text-xs text-ayush-charcoal font-medium">
                        {f.value}
                      </dd>
                    </div>
                  ))}
                </dl>
              )}
              {source.source_url && (
                <div className="mt-2">
                  <span className="text-xs text-gray-400 block mb-0.5">Source URL</span>
                  <a
                    href={source.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs text-ayush-green hover:underline break-all"
                  >
                    {source.source_url}
                  </a>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default function SourceList({ sources }) {
  if (!sources || sources.length === 0) return null

  return (
    <div>
      <h3 className="text-sm font-semibold text-ayush-charcoal mb-3">
        Retrieved Sources ({sources.length})
      </h3>
      <div className="space-y-2">
        {sources.map((source, i) => (
          <SourceItem key={i} source={source} index={i} />
        ))}
      </div>
    </div>
  )
}
