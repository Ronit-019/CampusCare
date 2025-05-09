document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("statusContainer");
  if (container) {
    // Mock data
    const grievances = [
      { title: "Library Access Issue", category: "Academic", status: "Resolved" },
      { title: "Hostel Food Quality", category: "Administrative", status: "Pending" },
    ];

    grievances.forEach(g => {
      const div = document.createElement("div");
      div.style.border = "1px solid #ccc";
      div.style.padding = "10px";
      div.style.marginBottom = "10px";
      div.innerHTML = `
        <strong>${g.title}</strong> (${g.category})<br>
        <em>Status: ${g.status}</em>
      `;
      container.appendChild(div);
    });
  }
});
