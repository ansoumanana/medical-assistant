import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const handleAsk = async () => {
    const res = await axios.post('https://YOUR_BACKEND_URL/ask', { question });
    setAnswer(res.data.answer);
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Assistant Médical</h1>
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        className="w-full border p-2"
        rows="4"
      />
      <button onClick={handleAsk} className="mt-2 px-4 py-2 bg-blue-600 text-white">
        Poser la question
      </button>
      {answer && <p className="mt-4 bg-gray-100 p-2 rounded">{answer}</p>}
    </div>
  );
}

export default App;
