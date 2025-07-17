import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [retrievedChunks, setRetrievedChunks] = useState([]);
  const [result, setResult] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleFileUpload = async () => {
    if (!file) return alert("Please select a file");
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:5000/upload", formData);
      alert(res.data.message);
    } catch (err) {
      console.error(err);
      alert("File upload failed");
    }
  };

  const handleQuery = async () => {
    if (!query.trim()) return alert("Please enter a query");

    setIsLoading(true);
    setRetrievedChunks([]);
    setResult("");

    try {
      const res = await axios.post("http://localhost:5000/query", { query });
      setRetrievedChunks(res.data.chunks || []);
      setResult(res.data.result || ""); // ✅ Important
    } catch (err) {
      console.error(err);
      alert("Query failed");
    }

    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-3xl mx-auto bg-white shadow-md rounded-lg p-6">
        <h1 className="text-2xl font-bold mb-6">📑 Insurance Claim Evaluator</h1>

        {/* File Upload */}
        <div className="mb-4">
          <label className="block font-medium mb-1">Upload PDF</label>
          <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />
          <button
            onClick={handleFileUpload}
            className="ml-2 px-4 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Upload File
          </button>
        </div>

        {/* Query Input */}
        <div className="mb-4">
          <label className="block font-medium mb-1">Enter Claim Query</label>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. 46M, knee surgery, Pune, 3-month policy"
            className="w-full p-2 border rounded"
          />
        </div>

        <button
          onClick={handleQuery}
          className="px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700"
        >
          {isLoading ? "🔍 Processing..." : "Submit Query"}
        </button>

        {/* Result Display */}
        {result ? (
          <div className="mt-6 p-4 bg-green-100 rounded">
            <h2 className="text-lg font-semibold mb-2">✅ Decision</h2>
            <p>{result}</p>
          </div>
        ) : retrievedChunks.length > 0 ? (
          <div className="mt-6">
            <h2 className="text-lg font-semibold mb-2">🔍 Retrieved Chunks</h2>
            <ul className="list-disc ml-5">
              {retrievedChunks.map((chunk, idx) => (
                <li key={idx} className="mb-1">
                  {chunk}
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <p className="text-yellow-600 mt-4">⚠️ No chunks found.</p>
        )}
      </div>
    </div>
  );
}

export default App;
