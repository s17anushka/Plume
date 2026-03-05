import { useState, useEffect } from 'react';
import './ResourcesPanel.css';

function ResourcesPanel({ onClose }) {
  const [resources, setResources] = useState(null);

  useEffect(() => {
    // In production, fetch from backend
    setResources({
      crisis_helplines: {
        india: [
          { name: "AASRA", phone: "91-9820466726", availability: "24/7" },
          { name: "iCall (TISS)", phone: "9152987821", availability: "Mon-Sat, 8am-10pm" },
          { name: "Vandrevala Foundation", phone: "9999666555", availability: "24/7" },
          { name: "Snehi", phone: "91-22-27546669", availability: "24/7" }
        ]
      },
      online_support: [
        { name: "Vandrevala Foundation", url: "https://www.vandrevalafoundation.com/", type: "Chat & Email" },
        { name: "Mann Talks", url: "https://www.manntalks.org/", type: "Community" },
        { name: "YourDOST", url: "https://yourdost.com/", type: "Counseling" }
      ],
      self_help: [
        { name: "Breathing (4-7-8)", description: "Breathe in 4 sec, hold 7 sec, out 8 sec" },
        { name: "Grounding (5-4-3-2-1)", description: "5 see, 4 touch, 3 hear, 2 smell, 1 taste" },
        { name: "Journaling", description: "Write freely about your thoughts" }
      ]
    });
  }, []);

  if (!resources) return null;

  return (
    <div className="resources-panel">
      <div className="panel-header">
        <h2>📚 Mental Health Resources</h2>
        <button onClick={onClose} className="close-btn">✕</button>
      </div>

      <div className="panel-content">
        <section className="resource-section">
          <h3>🆘 Crisis Helplines (India)</h3>
          {resources.crisis_helplines.india.map((helpline, i) => (
            <div key={i} className="resource-card">
              <div className="resource-info">
                <strong>{helpline.name}</strong>
                <span className="availability">{helpline.availability}</span>
              </div>
              <a href={`tel:${helpline.phone}`} className="resource-action">
                📞 {helpline.phone}
              </a>
            </div>
          ))}
        </section>

        <section className="resource-section">
          <h3>💬 Online Support</h3>
          {resources.online_support.map((service, i) => (
            <div key={i} className="resource-card">
              <div className="resource-info">
                <strong>{service.name}</strong>
                <span className="resource-type">{service.type}</span>
              </div>
              <a 
                href={service.url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="resource-action"
              >
                Visit →
              </a>
            </div>
          ))}
        </section>

        <section className="resource-section">
          <h3>🧘 Self-Help Techniques</h3>
          {resources.self_help.map((technique, i) => (
            <div key={i} className="resource-card technique">
              <strong>{technique.name}</strong>
              <p>{technique.description}</p>
            </div>
          ))}
        </section>

        <div className="emergency-note">
          <p><strong>⚠️ In Immediate Danger?</strong></p>
          <p>Call <strong>112</strong> or go to your nearest hospital emergency room</p>
        </div>
      </div>
    </div>
  );
}

export default ResourcesPanel;