(function () {
  "use strict";
  var root = document.documentElement;
  function $(s, c) { return (c || document).querySelector(s); }
  function $all(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function say(el, text, bad) { if (!el) return; el.textContent = text; el.classList.toggle("is-error", !!bad); }

  /* Gợi ý khi mở trong trình duyệt Facebook/TikTok/Zalo */
  if (/\binapp\b/.test(root.className)) { var tip = $("#inapp-tip"); if (tip) tip.hidden = false; }

  /* Đổi giao diện sáng/tối (lưu bằng localStorage, có try/catch) */
  var tbtn = $("#theme-toggle");
  if (tbtn) {
    tbtn.hidden = false;
    tbtn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) {}
    });
  }

  var status = $("#action-status");
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (resolve, reject) {
      var ta = document.createElement("textarea");
      ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy") ? resolve() : reject(new Error("copy")); }
      catch (e) { reject(e); } finally { document.body.removeChild(ta); }
    });
  }
  function pageUrl() { return location.href.split("#")[0]; }

  /* Nút sao chép link */
  var copyBtn = $("#copy-url");
  if (copyBtn) {
    copyBtn.hidden = false;
    copyBtn.addEventListener("click", function () {
      copyText(pageUrl()).then(
        function () { say(status, copyBtn.getAttribute("data-ok"), false); },
        function () { say(status, copyBtn.getAttribute("data-fail"), true); }
      );
    });
  }

  /* Nút chia sẻ: Web Share API, không có thì sao chép link */
  $all("#share-btn, #share-btn-2").forEach(function (btn) {
    btn.hidden = false;
    btn.addEventListener("click", function () {
      var fallback = function () {
        copyText(pageUrl()).then(
          function () { say(status, btn.getAttribute("data-copied"), false); },
          function () { say(status, btn.getAttribute("data-fail"), true); }
        );
        if (!status || !status.offsetParent) { var c = $("#contact"); if (c && btn.id === "share-btn") c.scrollIntoView(); }
      };
      if (navigator.share) {
        navigator.share({ title: btn.getAttribute("data-title"), url: pageUrl() }).catch(function (err) {
          if (err && err.name !== "AbortError") fallback();
        });
      } else { fallback(); }
    });
  });

  /* FAQ: mở mục khi nhảy tới #faq bằng nút dịch vụ */
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href="#faq"]');
    if (a) { var first = $(".faq details"); if (first) first.open = true; }
  });
})();
