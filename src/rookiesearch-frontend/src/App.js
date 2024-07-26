import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [searchHistory, setSearchHistory] = useState([]);
  const [darkMode, setDarkMode] = useState(false);
  const [userName, setUserName] = useState('');

  useEffect(() => {
    const savedHistory = localStorage.getItem('searchHistory');
    if (savedHistory) {
      setSearchHistory(JSON.parse(savedHistory));
    }

    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode) {
      setDarkMode(JSON.parse(savedDarkMode));
    }

    const savedUserName = localStorage.getItem('userName');
    if (savedUserName) {
      setUserName(savedUserName);
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('searchHistory', JSON.stringify(searchHistory));
  }, [searchHistory]);

  useEffect(() => {
    localStorage.setItem('darkMode', JSON.stringify(darkMode));
    if (darkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  }, [darkMode]);

  useEffect(() => {
    localStorage.setItem('userName', userName);
  }, [userName]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim() || !userName.trim()) return;

    setIsLoading(true);
    setAnswer('');
    try {
      const response = await fetch('http://localhost:8000/answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: question }),
      });
      const data = await response.json();
      setAnswer(data.answer);
      const newSearch = {
        question,
        userName,
        date: new Date().toLocaleString(),
      };
      setSearchHistory(prevHistory => [newSearch, ...prevHistory.slice(0, 4)]);
    } catch (error) {
      console.error('Error:', error);
      setAnswer('Error: Unable to fetch the answer. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleHistoryClick = (historicalQuestion) => {
    setQuestion(historicalQuestion);
  };

  const toggleDarkMode = () => {
    setDarkMode(prevMode => !prevMode);
  };

  return (
    <div className={`app ${darkMode ? 'dark-mode' : ''}`}>
      <header className="app-header">
        <h1>RookieSearch</h1>
        <button onClick={toggleDarkMode} className="dark-mode-toggle">
          {darkMode ? '☀️' : '🌙'}
        </button>
      </header>
      <main className="main-content">
        
        <form onSubmit={handleSubmit} className="search-form">
          <div className="user-input">
            <input
              type="text"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              placeholder="Enter your name"
              className="name-input"
            />
          </div>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Enter your question here..."
            rows="4"
            className="question-input"
          />
          <button type="submit" disabled={isLoading || !userName.trim()} className="search-button">
            {isLoading ? 'Searching...' : 'Search'}
          </button>
        </form>
        {answer && (
          <div className="answer-container">
            <h2>Answer:</h2>
            <p>{answer}</p>
          </div>
        )}
        {searchHistory.length > 0 && (
          <div className="history-container">
            <h3>Recent Searches:</h3>
            <ul>
              {searchHistory.map((item, index) => (
                <li key={index} onClick={() => handleHistoryClick(item.question)}>
                  <span className="history-question">{item.question}</span>
                  <span className="history-info">
                    by {item.userName} on {item.date}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
