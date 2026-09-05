export default function Disclaimer() {
  return (
    <footer className="border-t border-gray-200 bg-white py-6 px-4 mt-auto">
      <div className="max-w-3xl mx-auto">
        <p className="text-xs text-gray-400 text-center leading-relaxed">
          This system provides information based on its curated legal source corpus and is{" "}
          <strong className="font-medium">not a substitute for professional legal advice</strong>
          . The formulation classification and potential IPR routes are application-generated and
          do not constitute legal or regulatory determinations. The legal corpus must be kept
          current and verified against authoritative sources. Consult a qualified legal
          professional for any specific legal guidance.
        </p>
      </div>
    </footer>
  )
}
