import React, { useState, useEffect, useCallback } from 'react';

// Main component, must be named App and exported as default
const App = () => {
  // State hooks for managing user input, the hash result, and the loading status
  const [text, setText] = useState('Enter text here to generate SHA-256 hash...');
  const [hash, setHash] = useState('');
  const [loading, setLoading] = useState(false);

  // Function to convert the raw cryptographic output (ArrayBuffer) to a hex string
  const arrayBufferToHex = (buffer) => {
    // This maps the raw byte array into a human-readable 64-character hex string
    return Array.prototype.map.call(new Uint8Array(buffer), (x) => 
      // Ensure each byte is represented by two hexadecimal characters (e.g., 'A' becomes '0A')
      ('00' + x.toString(16)).slice(-2)
    ).join('');
  };

  // Async function to compute the SHA-256 hash, optimized with useCallback
  const computeSHA256 = useCallback(async (input) => {
    if (!input) {
      setHash('');
      return;
    }

    setLoading(true);
    try {
      // Step 1: Encode the input string into a byte array (Uint8Array)
      const msgUint8 = new TextEncoder().encode(input);
      
      // Step 2: Use the secure browser API (crypto.subtle) to hash the bytes
      const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);
      
      // Step 3: Convert the byte array result into a hex string for display
      const hashHex = arrayBufferToHex(hashBuffer);
      setHash(hashHex);
    } catch (error) {
      console.error("Hashing failed:", error);
      setHash("Error computing hash. Check console.");
    } finally {
      // Stop the loading indicator regardless of success or failure
      setLoading(false);
    }
  }, []); // Empty dependency array means this function is only created once

  // Effect to recalculate the hash whenever the text changes (using debouncing for performance)
  useEffect(() => {
    // Set a delay (300ms) after the user stops typing
    const handler = setTimeout(() => {
      computeSHA256(text);
    }, 300);

    // This cleanup function runs if the text changes again before the 300ms is up
    return () => clearTimeout(handler);
  }, [text, computeSHA256]); // Dependencies ensure it runs only when 'text' or 'computeSHA256' changes

  const handleTextChange = (e) => {
    setText(e.target.value);
  };

  const copyToClipboard = () => {
    if (hash) {
        // Create a temporary textarea element to hold the hash
        const textArea = document.createElement("textarea");
        textArea.value = hash;
        document.body.appendChild(textArea);
        // Select and copy the text
        textArea.select();
        try {
            document.execCommand('copy');
            // Log success instead of using alert()
            console.log('Hash copied to clipboard!'); 
        } catch (err) {
            console.error('Copy failed:', err);
        }
        // Clean up the temporary element
        document.body.removeChild(textArea);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-white shadow-2xl rounded-xl p-8 space-y-8">
        <header className="text-center">
          <h1 className="text-4xl font-extrabold text-indigo-700 font-inter">
            CertiVault - Secure Hashing Tool
          </h1>
          <p className="text-gray-500 mt-2">
            A tool for generating tamper-proof data hashes, key to digital verification.
          </p>
        </header>

        {/* Input Area */}
        <div className="space-y-4">
          <label htmlFor="input-text" className="block text-sm font-medium text-gray-700">
            Input Data (Text)
          </label>
          <textarea
            id="input-text"
            className="w-full p-4 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out font-mono resize-none"
            rows="6"
            value={text}
            onChange={handleTextChange}
            placeholder="Enter the data you want to hash..."
          ></textarea>
        </div>

        {/* Hash Output */}
        <div className="space-y-4">
          <label className="block text-sm font-medium text-gray-700 flex justify-between items-center">
            SHA-256 Hash Output
            {loading && (
              <span className="text-indigo-600 text-xs font-semibold animate-pulse">
                Calculating...
              </span>
            )}
          </label>
          <div className="relative">
            <input
              type="text"
              readOnly
              value={loading && text.length > 0 ? '...' : hash}
              className="w-full p-4 pr-16 bg-gray-100 border border-gray-200 rounded-lg text-sm font-mono text-gray-800 break-all"
              placeholder="Hash will appear here"
            />
            <button
              onClick={copyToClipboard}
              disabled={!hash}
              className={`absolute right-2 top-1/2 transform -translate-y-1/2 p-2 rounded-lg text-white transition duration-150 ${
                hash 
                  ? 'bg-indigo-600 hover:bg-indigo-700 shadow-md' 
                  : 'bg-gray-400 cursor-not-allowed'
              }`}
              title="Copy Hash"
            >
                {/* Copy Icon (Lucide/SVG equivalent) */}
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M7 9a2 2 0 012-2h6a2 2 0 012 2v6a2 2 0 01-2 2H9a2 2 0 01-2-2V9z" />
                    <path d="M5 3a2 2 0 00-2 2v6a2 2 0 002 2V5h6a2 2 0 00-2-2H5z" />
                </svg>
            </button>
          </div>
          <p className="text-xs text-gray-400 mt-2">
            SHA-256 hashes are 64 characters long and are widely used to ensure data integrity.
          </p>
        </div>
      </div>
    </div>
  );
};

export default App;
