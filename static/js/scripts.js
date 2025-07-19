document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("verifyForm");
    const spinner = document.getElementById("loadingSpinner");
    const btn = document.getElementById("submitBtn");

    form.addEventListener("submit", () => {
        spinner.classList.remove("d-none");
        btn.setAttribute("disabled", "disabled");
    });
});
