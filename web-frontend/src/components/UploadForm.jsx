import React, {useState} from 'react';

function UploadForm(){
  const [file, setFile] = useState(null);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleUpload = async (e) => {
    e.preventDefault();
    if(!file) return alert("Please select a file");
    const fd = new FormData();
    fd.append('file', file);

    const resp = await fetch('http://127.0.0.1:8000/api/upload/', {
      method: 'POST',
      body: fd,
      headers: {
        'Authorization': 'Basic ' + btoa(username + ":" + password)
      }
    });

    if(resp.ok){
      alert("Uploaded Successfully!");
    } else {
      alert("Failed: " + await resp.text());
    }
  };

  return (
    <form onSubmit={handleUpload}>
      <h3>Upload CSV</h3>
      <input placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)} />
      <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
      <input type="file" accept=".csv" onChange={e=>setFile(e.target.files[0])}/>
      <button type="submit">Upload CSV</button>
    </form>
  );
}

export default UploadForm;
