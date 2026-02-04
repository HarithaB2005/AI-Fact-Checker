import React, { useState } from 'react';
import axios from 'axios';

const FactCheckerUI = () => {
    // State for Text Analysis
    const [textInput, setTextInput] = useState('');
    const [textResult, setTextResult] = useState(null);

    // State for Image Analysis
    const [imageFile, setImageFile] = useState(null);
    const [imageResult, setImageResult] = useState(null);

    const handleTextAnalyze = async () => {
        try {
            // Replace with your actual backend endpoint for text analysis
            const response = await axios.post('http://localhost:5000/api/analyze-text', {
                claim: textInput,
            });
            setTextResult(response.data);
        } catch (error) {
            console.error('Error analyzing text:', error);
            setTextResult({ status: 'Error', message: 'Could not connect to server.' });
        }
    };

    const handleImageUpload = async () => {
        if (!imageFile) return;

        const formData = new FormData();
        formData.append('image', imageFile);

        try {
            // Replace with your actual backend endpoint for image analysis
            const response = await axios.post('http://localhost:5000/api/analyze-image', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setImageResult(response.data);
        } catch (error) {
            console.error('Error analyzing image:', error);
            setImageResult({ status: 'Error', message: 'Could not connect to server.' });
        }
    };

    return (
        <div className="bg-gray-900 min-h-screen text-gray-200 p-8 font-sans">
            <h1 className="text-4xl font-bold text-center mb-12 text-gray-100">FactChecker</h1>

            <div className="flex flex-col md:flex-row gap-8 max-w-5xl mx-auto">
                {/* Text Analysis Section */}
                <div className="bg-gray-800 p-6 rounded-lg shadow-xl flex-1 border border-gray-700">
                    <h2 className="text-2xl font-semibold mb-4 text-emerald-400">Text Analysis</h2>
                    <p className="text-gray-400 mb-4">Enter a claim or statement to verify.</p>
                    <textarea
                        className="w-full h-32 p-3 rounded-lg bg-gray-700 text-gray-100 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Enter text here..."
                        value={textInput}
                        onChange={(e) => setTextInput(e.target.value)}
                    />
                    <button
                        className="w-full mt-4 py-3 rounded-lg bg-blue-600 hover:bg-blue-700 font-bold transition-colors"
                        onClick={handleTextAnalyze}
                    >
                        Analyze Claim
                    </button>
                    {textResult && (
                        <div className="mt-6 p-4 rounded-lg bg-gray-700 border border-gray-600">
                            <h3 className="text-lg font-semibold mb-2">Result:</h3>
                            <p className={`font-bold ${textResult.status === 'True' ? 'text-green-400' : 'text-red-400'}`}>
                                Status: {textResult.status}
                            </p>
                            <p className="text-sm text-gray-300 mt-2">{textResult.message}</p>
                        </div>
                    )}
                </div>

                {/* Image Analysis Section */}
                <div className="bg-gray-800 p-6 rounded-lg shadow-xl flex-1 border border-gray-700">
                    <h2 className="text-2xl font-semibold mb-4 text-emerald-400">Image Analysis</h2>
                    <p className="text-gray-400 mb-4">Upload an image containing text for verification.</p>
                    <input
                        type="file"
                        accept="image/*"
                        className="w-full text-gray-400 bg-gray-700 rounded-lg p-2 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-500 file:text-white hover:file:bg-blue-600"
                        onChange={(e) => setImageFile(e.target.files[0])}
                    />
                    <button
                        className="w-full mt-4 py-3 rounded-lg bg-emerald-600 hover:bg-emerald-700 font-bold transition-colors"
                        onClick={handleImageUpload}
                    >
                        Upload & Analyze
                    </button>
                    {imageResult && (
                        <div className="mt-6 p-4 rounded-lg bg-gray-700 border border-gray-600">
                            <h3 className="text-lg font-semibold mb-2">Extracted Text & Result:</h3>
                            <p className="text-gray-300">
                                <span className="font-semibold text-gray-100">Extracted Text:</span> {imageResult.extractedText}
                            </p>
                            <p className={`font-bold ${imageResult.status === 'True' ? 'text-green-400' : 'text-red-400'} mt-2`}>
                                Status: {imageResult.status}
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default FactCheckerUI;