// Example when iterating over accounts data
accounts.forEach(account => {
  const tr = document.createElement("tr");
  tr.innerHTML = `
    <td>${account.id}</td>
    <td>${account.account_number}</td>
    <td>${account.account_type}</td>
    <td>${account.balance}</td>
    <td>${account.customer.name}</td> <!-- Display customer name -->
    <td>${new Date(account.created_at).toLocaleString()}</td>
  `;
  tableBody.appendChild(tr);
});
