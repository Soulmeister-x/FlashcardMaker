import React, { useState } from 'react';
import './App.css';

function App() {
  const [flashcards, setFlashcards] = useState([]);
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [words, setWords] = useState([]);
  const [inputWord, setInputWord] = useState('');

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError('');
    } else {
      setFile(null);
      setError('Bitte wählen Sie eine gültige PDF-Datei aus.');
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      setError('Bitte wählen Sie zuerst eine PDF-Datei aus.');
      return;
    }

    setIsLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/process-pdf', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setFlashcards(data);
    } catch (error) {
      console.error('Error:', error);
      setError('Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (event) => {
    setInputWord(event.target.value);
  };

  const handleInputSubmit = (event) => {
    event.preventDefault();
    if (inputWord.trim() !== '') {
      setWords([...words, inputWord.trim()]);
      setInputWord('');
    }
  };

  return (
    <div className="app-container">
      <h1>Flashcard Maker</h1>
      <form onSubmit={handleSubmit} className="upload-form">
        <input 
          type="file" 
          onChange={handleFileChange} 
          accept=".pdf" 
          className="file-input"
        />
        <button type="submit" disabled={!file || isLoading} className="submit-button">
          {isLoading ? 'Verarbeitung...' : 'PDF verarbeiten'}
        </button>
      </form>
      {error && <p className="error-message">{error}</p>}
      
      <div className="word-input-container">
        <form onSubmit={handleInputSubmit}>
          <input
            type="text"
            value={inputWord}
            onChange={handleInputChange}
            placeholder="Neues Wort eingeben"
            className="word-input"
          />
          <button type="submit" className="add-word-button">Hinzufügen</button>
        </form>
      </div>
      
      <div className="word-list">
        <h2>Wortliste</h2>
        <ul>
          {words.map((word, index) => (
            <li key={index}>{word}</li>
          ))}
        </ul>
      </div>

      <div className="flashcards-container">
        {flashcards.map((card, index) => (
          <div key={index} className="flashcard">
            <h3 className="flashcard-question">Frage: {card.frage}</h3>
            <p className="flashcard-answer">Antwort: {card.antwort}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
