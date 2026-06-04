// import { useState } from "react";
// import "./App.css";

// function App() {
//   const [spokenText, setSpokenText] = useState("");
//   const [patients, setPatients] = useState([]);
//   const [lastFilter, setLastFilter] = useState({});
//   const [error, setError] = useState("");
//   const [listening, setListening] = useState(false);
//   const [uploadResult, setUploadResult] = useState(null);

//   const sendToBackend = async (text) => {
//     setError("");

//     if (!text.trim()) {
//       setError("Please enter or speak something to search");
//       return;
//     }

//     try {
//       const response = await fetch("http://127.0.0.1:8000/voice-query", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({
//           text: text,
//           previous_filter: lastFilter,
//         }),
//       });

//       const data = await response.json();

//       if (!response.ok) {
//         setError(data.detail || "Something went wrong");
//         return;
//       }

//       setPatients(data.patients || []);
//       setLastFilter(data.applied_filter || {});
//     } catch (err) {
//       setError("Backend not running");
//     }
//   };

//   const uploadReport = async (file) => {
//     if (!file) return;

//     setError("");
//     setUploadResult(null);

//     const formData = new FormData();
//     formData.append("file", file);

//     try {
//       const response = await fetch("http://127.0.0.1:8000/upload-report", {
//         method: "POST",
//         body: formData,
//       });

//       const data = await response.json();

//       if (!response.ok) {
//         setError(data.detail || "PDF upload failed");
//         return;
//       }

//       setUploadResult(data);
//     } catch (err) {
//       setError("Backend not running");
//     }
//   };

//   const clearSearch = () => {
//     setSpokenText("");
//     setPatients([]);
//     setLastFilter({});
//     setError("");
//     setUploadResult(null);
//   };

//   const startListening = () => {
//     setError("");

//     const SpeechRecognition =
//       window.SpeechRecognition || window.webkitSpeechRecognition;

//     if (!SpeechRecognition) {
//       setError("Speech Recognition not supported in this browser");
//       return;
//     }

//     const recognition = new SpeechRecognition();
//     recognition.lang = "en-US";
//     recognition.interimResults = false;

//     recognition.start();
//     setListening(true);

//     recognition.onresult = async (event) => {
//       const transcript = event.results[0][0].transcript;
//       setSpokenText(transcript);
//       setListening(false);
//       await sendToBackend(transcript);
//     };

//     recognition.onerror = () => {
//       setListening(false);
//       setError("Voice recognition failed");
//     };

//     recognition.onend = () => {
//       setListening(false);
//     };
//   };

//   return (
//     <div className="container">
//       <h1>🎤 Voice Patient Information System</h1>

//       <input
//         type="text"
//         value={spokenText}
//         onChange={(e) => setSpokenText(e.target.value)}
//         placeholder="Enter the details you want to search"
//       />

//       <div>
//         <button onClick={startListening}>
//           {listening ? "Listening..." : "Start Speaking"}
//         </button>

//         <button onClick={() => sendToBackend(spokenText)}>Search</button>

//         <button onClick={clearSearch}>Clear</button>
//       </div>

//       <div className="upload-box">
//         <h3>Upload Medical Report</h3>
//         <input
//           type="file"
//           accept="application/pdf"
//           onChange={(e) => uploadReport(e.target.files[0])}
//         />
//       </div>

//       {uploadResult && (
//         <div className="filter-box">
//           <b>Uploaded Report:</b> {uploadResult.filename}
//           <pre>{JSON.stringify(uploadResult.ai_extracted_data, null, 2)}</pre>
//         </div>
//       )}

//       {spokenText && (
//         <p className="spoken">
//           <b>You said:</b> {spokenText}
//         </p>
//       )}

//       {Object.keys(lastFilter).length > 0 && (
//         <div className="filter-box">
//           <b>Current Filter:</b>
//           <pre>{JSON.stringify(lastFilter, null, 2)}</pre>
//         </div>
//       )}

//       {error && <p className="error">{error}</p>}

//       {patients.length > 0 && (
//         <div className="card">
//           <h2>Patient Results</h2>

//           {patients.map((item, index) => (
//             <div className="record" key={index}>
//               <h2 className="patient-name">Patient details : {item.name}</h2>

//               <div className="grid">
//                 <div className="info-item">
//                   <b>Gender:</b> {item.gender || "Not available"}
//                 </div>

//                 <div className="info-item">
//                   <b>Blood Group:</b> {item.blood_group || "Not available"}
//                 </div>

//                 <div className="info-item">
//                   <b>Contact:</b> {item.contact_number}
//                 </div>

//                 <div className="info-item">
//                   <b>Hospital:</b> {item.hospital}
//                 </div>
//               </div>

//               <h3 className="section-title">Medical Record</h3>

//               <div className="grid">
//                 <div className="info-item">
//                   <b>Disease:</b>{" "}
//                   {item.medical_record?.disease || "Not available"}
//                 </div>

//                 <div className="info-item">
//                   <b>Medicine:</b>{" "}
//                   {item.medical_record?.medicine || "Not available"}
//                 </div>

//                 <div className="info-item">
//                   <b>Doctor:</b>{" "}
//                   {item.medical_record?.doctor_name || "Not available"}
//                 </div>

//                 <div className="info-item">
//                   <b>Visit Date:</b>{" "}
//                   {item.medical_record?.visit_date || "Not available"}
//                 </div>

//                 <div className="info-item">
//                   <b>Dosage:</b>{" "}
//                   {item.medical_record?.dosage || "Not available"}
//                 </div>

//                 <div className="info-item">
//                   <b>Lab Test:</b>{" "}
//                   {item.medical_record?.lab_tests || "Not available"}
//                 </div>

//                 <div className="info-item">
//                   <b>Test Result:</b>{" "}
//                   {item.medical_record?.test_results || "Not available"}
//                 </div>

//                 <div className="info-item">
//                   <b>Number of Visits:</b>{" "}
//                   {item.medical_record?.follow_up_required ?? 0}
//                 </div>

//                 <div className="info-item">
//                   <b>Next Visit:</b>{" "}
//                   {item.medical_record?.follow_up_date || "No Visit"}
//                 </div>
//               </div>
//             </div>
//           ))}
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

import { useState } from "react";
import jsPDF from "jspdf";
import "./App.css";

function App() {
  const [spokenText, setSpokenText] = useState("");
  const [patients, setPatients] = useState([]);
  const [lastFilter, setLastFilter] = useState({});
  const [error, setError] = useState("");
  const [listening, setListening] = useState(false);
 

  const sendToBackend = async (text) => {
    setError("");

    if (!text.trim()) {
      setError("Please enter or speak something to search");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/voice-query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: text,
          previous_filter: lastFilter,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Something went wrong");
        return;
      }

      setPatients(data.patients || []);
      setLastFilter(data.applied_filter || {});
    } catch (err) {
      setError("Backend not running");
    }
  };

  const downloadPatientPDF = (item) => {
    const doc = new jsPDF();

    doc.setFontSize(18);
    doc.text("Patient Medical Report", 20, 20);

    doc.setFontSize(12);
    let y = 35;

    doc.text(`Name: ${item.name}`, 20, y); y += 10;
    doc.text(`Gender: ${item.gender || "Not available"}`, 20, y); y += 10;
    doc.text(`Blood Group: ${item.blood_group || "Not available"}`, 20, y); y += 10;
    doc.text(`Contact: ${item.contact_number}`, 20, y); y += 10;
    doc.text(`Hospital: ${item.hospital}`, 20, y); y += 15;

    doc.setFontSize(14);
    doc.text("Medical Record", 20, y); y += 10;

    doc.setFontSize(12);
    doc.text(`Disease: ${item.medical_record?.disease || "Not available"}`, 20, y); y += 10;
    doc.text(`Medicine: ${item.medical_record?.medicine || "Not available"}`, 20, y); y += 10;
    doc.text(`Doctor: ${item.medical_record?.doctor_name || "Not available"}`, 20, y); y += 10;
    doc.text(`Visit Date: ${item.medical_record?.visit_date || "Not available"}`, 20, y); y += 10;
    doc.text(`Dosage: ${item.medical_record?.dosage || "Not available"}`, 20, y); y += 10;
    doc.text(`Lab Test: ${item.medical_record?.lab_tests || "Not available"}`, 20, y); y += 10;
    doc.text(`Test Result: ${item.medical_record?.test_results || "Not available"}`, 20, y); y += 10;
    doc.text(`Number of Visits: ${item.medical_record?.follow_up_required ?? 0}`, 20, y); y += 10;
    doc.text(`Next Visit: ${item.medical_record?.follow_up_date || "No Visit"}`, 20, y);

    doc.save(`${item.name}_medical_report.pdf`);
  };

  const clearSearch = () => {
    setSpokenText("");
    setPatients([]);
    setLastFilter({});
    setError("");
  };

  const startListening = () => {
    setError("");

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setError("Speech Recognition not supported in this browser");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;

    recognition.start();
    setListening(true);

    recognition.onresult = async (event) => {
      const transcript = event.results[0][0].transcript;
      setSpokenText(transcript);
      setListening(false);
      await sendToBackend(transcript);
    };

    recognition.onerror = () => {
      setListening(false);
      setError("Voice recognition failed");
    };

    recognition.onend = () => {
      setListening(false);
    };
  };



    
  return (
    <div className="container">
      <h1> Voice Patient Information System</h1>

      <input
        type="text"
        value={spokenText}
        onChange={(e) => setSpokenText(e.target.value)}
        placeholder="Enter the Details you want to search"
      />

      <div>
        <button onClick={startListening}>
          {listening ? "Listening..." : "Start Speaking"}
        </button>

        <button onClick={() => sendToBackend(spokenText)}>Search</button>

        <button onClick={clearSearch}>Clear</button>
      </div>

      {spokenText && (
        <p className="spoken">
          <b>You said:</b> {spokenText}
        </p>
      )}

      {/* {Object.keys(lastFilter).length > 0 && (
        <div className="filter-box">
          <b>Current Filter:</b>
          <pre>{JSON.stringify(lastFilter, null, 2)}</pre>
        </div>
      )} */}

      {error && <p className="error">{error}</p>}

      {patients.length > 0 && (
        <div className="card">
          <h2>Patient Results</h2>

          {patients.map((item, index) => (
            <div className="record" key={index}>
              <h2 className="patient-name">Patient details : {item.name}</h2>

              <button onClick={() => downloadPatientPDF(item)}>
                Download PDF
              </button>

              <div className="grid">
                <div className="info-item">
                  <b>Gender:</b> {item.gender || "Not available"}
                </div>

                <div className="info-item">
                  <b>Blood Group:</b> {item.blood_group || "Not available"}
                </div>

                <div className="info-item">
                  <b>Contact:</b> {item.contact_number}
                </div>

                <div className="info-item">
                  <b>Hospital:</b> {item.hospital}
                </div>


                
              </div>

              <h3 className="section-title">Medical Record</h3>

              <div className="grid">
                <div className="info-item">
                  <b>Disease:</b> {item.medical_record?.disease || "Not available"}
                </div>

                <div className="info-item">
                  <b>Medicine:</b> {item.medical_record?.medicine || "Not available"}
                </div>

                <div className="info-item">
                  <b>Doctor:</b> {item.medical_record?.doctor_name || "Not available"}
                </div>

                <div className="info-item">
                  <b>Visit Date:</b> {item.medical_record?.visit_date || "Not available"}
                </div>

                <div className="info-item">
                  <b>Dosage:</b> {item.medical_record?.dosage || "Not available"}
                </div>

                <div className="info-item">
                  <b>Lab Test:</b> {item.medical_record?.lab_tests || "Not available"}
                </div>

                <div className="info-item">
                  <b>Test Result:</b> {item.medical_record?.test_results || "Not available"}
                </div>

                <div className="info-item">
                  <b>Number of Visits:</b>{" "}
                  {item.medical_record?.follow_up_required ?? 0}
                </div>

                <div className="info-item">
                  <b>Next Visit:</b>{" "}
                  {item.medical_record?.follow_up_date || "No Visit"}
                </div>
                
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;