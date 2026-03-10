// import React, { useState, useEffect } from 'react';
// import '../styles/Dashboard.css'; // CSS file
// import { Link } from 'react-router-dom';
// import { useNavigate } from "react-router-dom";


// const Dashboard = () => {
//   const navigate = useNavigate();

//   const handleLogin = () => {
//     navigate("/");
//   };
//   const [leads, setLeads] = useState([]);
//   const [activeTab, setActiveTab] = useState('leads');
//   const [searchTerm, setSearchTerm] = useState('');
//   const [filterStatus, setFilterStatus] = useState('All');

// //   useEffect(() => {
// //     const mockLeads = [
// //       { name: "Ha**** Li****", contactInfo: "(1**********)", propertyAddress: "Fa***************", status: "Open" },
// //       { name: "Ma*** Or****", contactInfo: "(1**********)", propertyAddress: "Fa***************", status: "Open" },
// //       { name: "Ki**** Ly***", contactInfo: "(1**********)", propertyAddress: "Fa***************", status: "Open" },
// //       { name: "Mara Holloway", contactInfo: "(167) 278-5282", propertyAddress: "Fairfax Radiology Center of...", status: "Open" },
// //       { name: "Zenia Howard", contactInfo: "(128) 520-4825", propertyAddress: "Fairfax Radiology Center of...", status: "Open" },
// //       { name: "Xandra Cotton", contactInfo: "(130) 185-1921", propertyAddress: "Fairfax Radiology Center of...", status: "Open" }
// //     ];
// //     setLeads(mockLeads);
// //   }, []);
// //   useEffect(() => {
// //   fetch("http://127.0.0.1:9000/leads")
// //     .then((res) => res.json())
// //     .then((data) => setLeads(data))
// //     .catch((err) => console.error(err));
// // }, [leads]);

//   useEffect(() => {
//     // Function to fetch data
//     const fetchLeads = () => {
//       fetch("http://127.0.0.1:9000/leads")
//         .then((res) => res.json())
//         .then((data) => setLeads(data))
//         .catch((err) => console.error(err));
//     };
// // # web socket
//     // First call immediately
//     fetchLeads();

//     // Poll every 5 seconds
//     const interval = setInterval(fetchLeads, 500000);

//     // Cleanup interval on component unmount
//     return () => clearInterval(interval);
//   }, []); // Empty dependency → no infinite loop

//   // Filtered leads based on search + dropdown
//   const filteredLeads = leads.filter(lead => 
//     (lead.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
//     lead.propertyAddress.toLowerCase().includes(searchTerm.toLowerCase())) &&
//     (filterStatus === 'All' || lead.status === filterStatus)
//   );

//   return (
//     <div className="dashboard-container">
//       {/* Sidebar */}
//       <div className="sidebar">
//         <div className="sidebar-header">
//           <h2>RoofClaimPros</h2>
//         </div>
//         <ul className="sidebar-menu">
//           <li><a className={activeTab === 'dashboard' ? 'active' : ''} onClick={() => setActiveTab('dashboard')}>Dashboard</a></li>
//           <li><a className={activeTab === 'crm' ? 'active' : ''} style={{pointerEvents:'none', opacity:0.5}}>CRM</a></li>
//           <li><a className={activeTab === 'leads' ? 'active' : ''} onClick={() => setActiveTab('leads')}>Leads</a></li>
//           <li><a className={activeTab === 'appointments' ? 'active' : ''} style={{pointerEvents:'none', opacity:0.5}}>Appointments</a></li>
//           <li><a className={activeTab === 'settings' ? 'active' : ''} style={{pointerEvents:'none', opacity:0.5}}>Settings</a></li>
//           <button id = "logout" className='primary-btn' onClick={handleLogin}><li><a href="#">Logout</a></li></button>
//         </ul>
//       </div>

//       {/* Main Content */}
//       <div className="main-content">
//         {activeTab === 'leads' && (
//           <div className="leads-container">
//             <h2>My Purchased Leads</h2>
//             <p>Manage and track your purchased leads and their progress</p>

//             {/* Search + Dropdown */}
//             <div className="search-filter">
//               <input
//                 type="text"
//                 placeholder="Search leads..."
//                 value={searchTerm}
//                 onChange={(e) => setSearchTerm(e.target.value)}
//               />
//               <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
//                 <option value="All">All</option>
//                 <option value="Open">Open</option>
//                 <option value="Closed">hot weather</option>
//                 <option value="Closed">cool weather</option>
//               </select>
//             </div>

//             {/* Leads Table */}
//             <div className="leads-list">
//               <table>
//                 <thead>
//                   <tr>
//                     <th>Name</th>
//                     <th>Contact Info</th>
//                     <th>Property Address</th>
//                     <th>Status</th>
//                     <th>Action</th>
//                   </tr>
//                 </thead>
//                 <tbody>
//                   {filteredLeads.length > 0 ? filteredLeads.map((lead, index) => (
//                     <tr key={index}>
//                       <td>{lead.name}</td>
//                       <td>{lead.contactInfo}</td>
//                       <td>{lead.propertyAddress}</td>
//                       <td>{lead.status}</td>
//                       <td><button className="buy-btn">View Now</button></td>
//                     </tr>
//                   )) : (
//                     <tr>
//                       <td colSpan="5">No leads found</td>
//                     </tr>
//                   )}
//                 </tbody>
//               </table>
//             </div>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

// export default Dashboard;

// import React, { useState, useEffect } from 'react';
// import '../styles/Dashboard.css'; 
// import { useNavigate } from "react-router-dom";

// const Dashboard = () => {
//   const navigate = useNavigate();
//   const handleLogin = () => navigate("/");

//   const [leads, setLeads] = useState([]);
//   const [activeTab, setActiveTab] = useState('leads');
//   const [searchTerm, setSearchTerm] = useState('');
//   const [filterStatus, setFilterStatus] = useState('All');

//   // Modal state
//   const [selectedLead, setSelectedLead] = useState(null);
//   const [showModal, setShowModal] = useState(false);

//   // Fetch leads with polling
//   useEffect(() => {
//     const fetchLeads = () => {
//       fetch("http://127.0.0.1:9000/leads")
//         .then(res => res.json())
//         .then(data => setLeads(data))
//         .catch(err => console.error(err));
//     };

//     fetchLeads();
//     const interval = setInterval(fetchLeads, 5000); // every 5 sec
//     return () => clearInterval(interval);
//   }, []);

//   // Filtered leads
//   const filteredLeads = leads.filter(lead => 
//     (lead.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
//      lead.propertyAddress.toLowerCase().includes(searchTerm.toLowerCase())) &&
//     (filterStatus === 'All' || lead.status === filterStatus)
//   );

//   return (
//     <div className="dashboard-container">
//       {/* Sidebar */}
//       <div className="sidebar">
//         <div className="sidebar-header"><h2>RoofClaimPros</h2></div>
//         <ul className="sidebar-menu">
//           <li><a className={activeTab==='dashboard'?'active':''} onClick={()=>setActiveTab('dashboard')}>Dashboard</a></li>
//           <li><a className={activeTab==='crm'?'active':''} style={{pointerEvents:'none',opacity:0.5}}>CRM</a></li>
//           <li><a className={activeTab==='leads'?'active':''} onClick={()=>setActiveTab('leads')}>Leads</a></li>
//           <li><a className={activeTab==='appointments'?'active':''} style={{pointerEvents:'none',opacity:0.5}}>Appointments</a></li>
//           <li><a className={activeTab==='settings'?'active':''} style={{pointerEvents:'none',opacity:0.5}}>Settings</a></li>
//           <button className='primary-btn' onClick={handleLogin}><li><a href="#">Logout</a></li></button>
//         </ul>
//       </div>

//       {/* Main Content */}
//       <div className="main-content">
//         {activeTab === 'leads' && (
//           <div className="leads-container">
//             <h2>My Purchased Leads</h2>
//             <p>Manage and track your purchased leads and their progress</p>

//             {/* Search + Dropdown */}
//             <div className="search-filter">
//               <input
//                 type="text"
//                 placeholder="Search leads..."
//                 value={searchTerm}
//                 onChange={e=>setSearchTerm(e.target.value)}
//               />
//               <select value={filterStatus} onChange={e=>setFilterStatus(e.target.value)}>
//                 <option value="All">All</option>
//                 <option value="Open">Open</option>
//                 <option value="Close">Close</option>
//                 <option value="hot">Hot Weather</option>
//                 <option value="Cool">Cool Weather</option>
          
//               </select>
//             </div>

//             {/* Leads Table */}
//             <div className="leads-list">
//               <table>
//                 <thead>
//                   <tr>
//                     <th>Name</th>
//                     <th>Contact Info</th>
//                     <th>Property Address</th>
//                     <th>Status</th>
//                     <th>Action</th>
//                   </tr>
//                 </thead>
//                 <tbody>
//                   {filteredLeads.length > 0 ? filteredLeads.map((lead,index)=>(
//                     <tr key={index}>
//                       <td>{lead.name}</td>
//                       <td>{lead.contactInfo}</td>
//                       <td>{lead.propertyAddress}</td>
//                       <td>{lead.status}</td>
//                       <td>
//                         <button 
//                           className="buy-btn"
//                           onClick={()=>{setSelectedLead(lead); setShowModal(true);}}
//                         >View Now</button>
//                       </td>
//                     </tr>
//                   )):(
//                     <tr><td colSpan="5">No leads found</td></tr>
//                   )}
//                 </tbody>
//               </table>
//             </div>
//           </div>
//         )}
//       </div>

//       {/* Modal */}
//       {showModal && selectedLead && (
//         <div className="modal-overlay">
//           <div className="modal-box">
//             <h3>Lead Details</h3>
//             <p><strong>Name:</strong> {selectedLead.name}</p>
//             <p><strong>Contact:</strong> {selectedLead.contactInfo}</p>
//             <p><strong>Address:</strong> {selectedLead.propertyAddress}</p>
//             <p><strong>Status:</strong> {selectedLead.status}</p>
//             <button className="close-btn" onClick={()=>setShowModal(false)}>Close</button>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default Dashboard;


import React, { useState, useEffect } from 'react';
import '../styles/Dashboard.css'; 
import { useNavigate } from "react-router-dom";

const Dashboard = () => {

  const navigate = useNavigate();
  const handleLogin = () => navigate("/");

  const [leads, setLeads] = useState([]);
  const [activeTab, setActiveTab] = useState('leads');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('All');

  const [selectedLead, setSelectedLead] = useState(null);
  const [showModal, setShowModal] = useState(false);

  // NEW STATES
  const [showAddModal, setShowAddModal] = useState(false);

  const [newLead, setNewLead] = useState({
    name:"",
    contactInfo:"",
    propertyAddress:"",
    status:"Open"
  });

  // Fetch leads
  useEffect(() => {

    const fetchLeads = () => {
      fetch("http://127.0.0.1:9000/leads")
      .then(res => res.json())
      .then(data => setLeads(data))
      .catch(err => console.error(err));
    };

    fetchLeads();

    const interval = setInterval(fetchLeads, 500000);

    return () => clearInterval(interval);

  }, []);

  // DELETE FUNCTION
  const deleteLead = async (index) => {

    try{

      await fetch(`http://127.0.0.1:9000/leads/${index}`,{
        method:"DELETE"
      });

      setLeads(prev => prev.filter((_,i)=> i !== index));

    }catch(err){
      console.error(err);
    }

  };


  // ADD LEAD FUNCTION
  const handleAddLead = async () => {

    try{

      await fetch("http://127.0.0.1:9000/leads",{

        method:"POST",

        headers:{
          "Content-Type":"application/json"
        },

        body:JSON.stringify(newLead)

      });

      setLeads([...leads,newLead]);

      setShowAddModal(false);

      setNewLead({
        name:"",
        contactInfo:"",
        propertyAddress:"",
        status:"Open"
      });

    }catch(err){

      console.error(err);

    }

  };


  const filteredLeads = leads.filter(lead => 

    (lead.name.toLowerCase().includes(searchTerm.toLowerCase()) ||

     lead.propertyAddress.toLowerCase().includes(searchTerm.toLowerCase()))

     &&

     (filterStatus === 'All' || lead.status === filterStatus)

  );


  return (

    <div className="dashboard-container">

      {/* Sidebar */}

      <div className="sidebar">

        <div className="sidebar-header">

          <h2>RoofClaimPros</h2>

        </div>

        <ul className="sidebar-menu">

          <li><a className={activeTab==='dashboard'?'active':''} onClick={()=>setActiveTab('dashboard')}>Dashboard</a></li>

          <li><a className={activeTab==='crm'?'active':''} style={{pointerEvents:'none',opacity:0.5}}>CRM</a></li>

          <li><a className={activeTab==='leads'?'active':''} onClick={()=>setActiveTab('leads')}>Leads</a></li>

          <li><a className={activeTab==='appointments'?'active':''} style={{pointerEvents:'none',opacity:0.5}}>Appointments</a></li>

          <li><a className={activeTab==='settings'?'active':''} style={{pointerEvents:'none',opacity:0.5}}>Settings</a></li>

          <button className='primary-btn' onClick={handleLogin}><li><a href="#">Logout</a></li></button>

        </ul>

      </div>


      {/* Main */}

      <div className="main-content">

        {activeTab === 'leads' && (

          <div className="leads-container">

            <h2>My Purchased Leads</h2>

            <p>Manage and track your purchased leads and their progress</p>


            {/* ADD BUTTON */}

            <button className="add-btn" onClick={()=>setShowAddModal(true)}>
              + Add Lead
            </button>


            {/* Search */}

            <div className="search-filter">

              <input
                type="text"
                placeholder="Search leads..."
                value={searchTerm}
                onChange={e=>setSearchTerm(e.target.value)}
              />


              <select value={filterStatus} onChange={e=>setFilterStatus(e.target.value)}>

                <option value="All">All</option>
                <option value="Open">Open</option>
                <option value="Close">Close</option>
                <option value="hot">Hot Weather</option>
                <option value="Cool">Cool Weather</option>

              </select>

            </div>


            {/* Table */}

            <div className="leads-list">

              <table>

                <thead>

                  <tr>

                    <th>Name</th>
                    <th>Contact Info</th>
                    <th>Property Address</th>
                    <th>Status</th>
                    <th>Action</th>

                  </tr>

                </thead>

                <tbody>

                {filteredLeads.length > 0 ?

                filteredLeads.map((lead,index)=>(

                  <tr key={index}>

                    <td>{lead.name}</td>
                    <td>{lead.contactInfo}</td>
                    <td>{lead.propertyAddress}</td>
                    <td>{lead.status}</td>

                    <td>

                      <button
                        className="buy-btn"
                        onClick={()=>{setSelectedLead(lead);setShowModal(true);}}
                      >
                        View Now
                      </button>

                      <button
                        className="delete-btn"
                        onClick={()=>deleteLead(index)}
                      >
                        Delete
                      </button>

                    </td>

                  </tr>

                ))

                :

                <tr><td colSpan="5">No leads found</td></tr>

                }

                </tbody>

              </table>

            </div>

          </div>

        )}

      </div>


      {/* VIEW MODAL */}

      {showModal && selectedLead && (

        <div className="modal-overlay">

          <div className="modal-box">

            <h3>Lead Details</h3>

            <p><strong>Name:</strong> {selectedLead.name}</p>
            <p><strong>Contact:</strong> {selectedLead.contactInfo}</p>
            <p><strong>Address:</strong> {selectedLead.propertyAddress}</p>
            <p><strong>Status:</strong> {selectedLead.status}</p>

            <button className="close-btn" onClick={()=>setShowModal(false)}>Close</button>

          </div>

        </div>

      )}


      {/* ADD MODAL */}

      {/* {showAddModal && (

        <div className="modal-overlay">

          <div className="modal-box">

            <h3>Add New Lead</h3>

            <input
              type="text"
              placeholder="Name"
              value={newLead.name}
              onChange={(e)=>setNewLead({...newLead,name:e.target.value})}
            />

            <input
              type="text"
              placeholder="Contact Info"
              value={newLead.contactInfo}
              onChange={(e)=>setNewLead({...newLead,contactInfo:e.target.value})}
            />

            <input
              type="text"
              placeholder="Property Address"
              value={newLead.propertyAddress}
              onChange={(e)=>setNewLead({...newLead,propertyAddress:e.target.value})}
            />

            <select
              value={newLead.status}
              onChange={(e)=>setNewLead({...newLead,status:e.target.value})}
            >

              <option>Open</option>
              <option>Close</option>
              <option>Hot</option>
              <option>Cool</option>

            </select>

            <button onClick={handleAddLead}>Submit</button>

            <button onClick={()=>setShowAddModal(false)}>Cancel</button>

          </div>

        </div>

      )} */}

    {showAddModal && (

  <div className="modal-overlay">

    <div className="modal-box">

      <h3>Add New Lead</h3>

      <input
        type="text"
        placeholder="Name"
        value={newLead.name}
        onChange={(e)=>{
          const value = e.target.value;

          // allow only alphabets and spaces
          if(/^[a-zA-Z\s]*$/.test(value)){
            setNewLead({...newLead,name:value});
          }
        }}
      />

      <input
        type="text"
        placeholder="Contact Info"
        value={newLead.contactInfo}
        onChange={(e)=>{
          const value = e.target.value;

          // allow only numbers
          if(/^[0-9]*$/.test(value)){
            setNewLead({...newLead,contactInfo:value});
          }
        }}
      />

      <input
        type="text"
        placeholder="Property Address"
        value={newLead.propertyAddress}
        onChange={(e)=>setNewLead({...newLead,propertyAddress:e.target.value})}
      />

      <select
        value={newLead.status}
        onChange={(e)=>setNewLead({...newLead,status:e.target.value})}
      >

        <option>Open</option>
        <option>Close</option>
        <option>Hot</option>
        <option>Cool</option>

      </select>

      <button onClick={handleAddLead}>Submit</button>

      <button onClick={()=>setShowAddModal(false)}>Cancel</button>

    </div>

  </div>

)}

    </div>

  );

};

export default Dashboard;