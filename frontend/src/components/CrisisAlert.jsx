import './CrisisAlert.css';

function CrisisAlert({ level }) {
  const getMessage = () => {
    if (level >= 9) {
      return {
        title: '🆘 Immediate Support Available',
        text: 'Please reach out to a crisis counselor right now.',
        urgency: 'emergency'
      };
    } else if (level >= 7) {
      return {
        title: '⚠️ Support Resources Available',
        text: 'We\'re concerned about you. Help is available 24/7.',
        urgency: 'severe'
      };
    } else {
      return {
        title: '💙 You\'re Not Alone',
        text: 'Support is available if you need it.',
        urgency: 'elevated'
      };
    }
  };

  const alert = getMessage();

  return (
    <div className={`crisis-alert ${alert.urgency}`}>
      <div className="alert-content">
        <h3>{alert.title}</h3>
        <p>{alert.text}</p>
        <div className="alert-actions">
          <a href="tel:9152987821" className="crisis-btn primary">
            📞 Call Now: 9152987821
          </a>
          <a 
            href="https://www.vandrevalafoundation.com/" 
            target="_blank" 
            rel="noopener noreferrer"
            className="crisis-btn secondary"
          >
            💬 Chat Online
          </a>
        </div>
      </div>
    </div>
  );
}

export default CrisisAlert;