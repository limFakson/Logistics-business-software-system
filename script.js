const searchInput = document.getElementById("searchInput");
  const statusFilter = document.getElementById("statusFilter");
  const cards = document.querySelectorAll(".order-card");

  function filterOrders() {
    const query = searchInput.value.toLowerCase();
    const status = statusFilter.value;

    cards.forEach(card => {
      const content = card.textContent.toLowerCase();
      const cardStatus = card.dataset.status;

      const matchText = content.includes(query);
      const matchStatus = (status === "all" || status === cardStatus);

      card.style.display = (matchText && matchStatus) ? "block" : "none";
    });
  }

  searchInput.addEventListener("input", filterOrders);
  statusFilter.addEventListener("change", filterOrders);


