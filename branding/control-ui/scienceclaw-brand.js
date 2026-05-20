(function () {
  var icon = "./scienceclaw-icon.png";
  var replacements = [
    ["OpenClaw Control", "ScienceClaw"],
    ["OpenClaw Scientific Working Group", "ScienceClaw Scientific Working Group"],
    ["OpenClaw", "ScienceClaw"],
    ["ESIILclaw Scientific Working Group", "ScienceClaw Scientific Working Group"],
    ["ESIILclaw", "ScienceClaw"],
    ["Gateway Dashboard", "ScienceClaw Gateway"],
  ];

  function replaceExactText(root) {
    var walker = document.createTreeWalker(root || document.body, NodeFilter.SHOW_TEXT);
    var nodes = [];
    var node;
    while ((node = walker.nextNode())) nodes.push(node);
    nodes.forEach(function (textNode) {
      var value = textNode.nodeValue;
      if (!value) return;
      var next = value;
      replacements.forEach(function (pair) {
        next = next.split(pair[0]).join(pair[1]);
      });
      if (next !== value) textNode.nodeValue = next;
    });
  }

  function updateHead() {
    document.title = "ScienceClaw";
    document.documentElement.setAttribute("data-theme-mode", "light");
    document.documentElement.classList.add("scienceclaw-branded");

    Array.prototype.forEach.call(document.querySelectorAll('link[rel~="icon"], link[rel="apple-touch-icon"]'), function (link) {
      link.href = icon;
      if (link.rel === "apple-touch-icon") link.sizes = "180x180";
    });

    var theme = document.querySelector('meta[name="theme-color"]');
    if (!theme) {
      theme = document.createElement("meta");
      theme.name = "theme-color";
      document.head.appendChild(theme);
    }
    theme.content = "#234a65";
  }

  function updateAttributes() {
    Array.prototype.forEach.call(document.querySelectorAll("[aria-label], [alt], [placeholder], [title]"), function (el) {
      ["aria-label", "alt", "placeholder", "title"].forEach(function (attr) {
        var value = el.getAttribute(attr);
        if (!value) return;
        var next = value;
        replacements.forEach(function (pair) {
          next = next.split(pair[0]).join(pair[1]);
        });
        if (next !== value) el.setAttribute(attr, next);
      });
    });
  }

  function installBrandPlate() {
    if (document.querySelector(".scienceclaw-brand-plate")) return;
    var candidates = Array.prototype.slice.call(document.querySelectorAll("header, nav, [class*=header], [class*=topbar], [class*=breadcrumb]"));
    var host = candidates.find(function (el) {
      var rect = el.getBoundingClientRect();
      return rect.width > 240 && rect.height > 32 && rect.top < 140;
    });
    if (!host) return;

    var plate = document.createElement("div");
    plate.className = "scienceclaw-brand-plate";
    plate.setAttribute("aria-label", "OASIS ScienceClaw");
    plate.innerHTML =
      '<img src="' + icon + '" alt="" />' +
      '<span class="scienceclaw-brand-lockup">' +
      '<strong>OASIS ScienceClaw</strong>' +
      "<small>ESIIL's multi-agent workspace</small>" +
      '</span>';
    host.insertBefore(plate, host.firstChild);
  }

  function getProjectTitle() {
    var stored = "";
    try {
      stored = window.localStorage.getItem("scienceclaw.projectTitle") || "";
    } catch (_) {
      stored = "";
    }
    return (
      stored.trim() ||
      (window.SCIENCECLAW_CONFIG && window.SCIENCECLAW_CONFIG.projectTitle || "").trim() ||
      (window.SCIENCECLAW_PROJECT_TITLE || "").trim() ||
      "OASIS ScienceClaw Working Group"
    );
  }

  function setProjectTitle(value) {
    var title = (value || "").trim() || "OASIS ScienceClaw Working Group";
    try {
      window.localStorage.setItem("scienceclaw.projectTitle", title);
    } catch (_) {
      // The banner still updates for the current page even if localStorage is unavailable.
    }
    window.SCIENCECLAW_PROJECT_TITLE = title;
    window.SCIENCECLAW_CONFIG = window.SCIENCECLAW_CONFIG || {};
    window.SCIENCECLAW_CONFIG.projectTitle = title;
    return title;
  }

  function findControlRow() {
    var controls = Array.prototype.slice.call(document.querySelectorAll("input, select, button, [role='button']"));
    var candidates = controls
      .map(function (el) {
        var node = el;
        for (var depth = 0; node && depth < 6; depth += 1, node = node.parentElement) {
          var rect = node.getBoundingClientRect();
          if (rect.top > 70 && rect.top < 230 && rect.width > window.innerWidth * 0.45 && rect.height >= 36 && rect.height < 120) {
            return node;
          }
        }
        return null;
      })
      .filter(Boolean);

    return candidates.find(function (el) {
      var text = (el.textContent || "").toLowerCase();
      return text.indexOf("pi liaison") !== -1 || text.indexOf("ai-verde") !== -1 || text.indexOf("main") !== -1;
    }) || candidates[0] || findControlRowByText();
  }

  function findControlRowByText() {
    var nodes = Array.prototype.slice.call(document.querySelectorAll("header *, main *, [class*=header] *, [class*=toolbar] *"));
    return nodes.find(function (el) {
      var rect = el.getBoundingClientRect();
      var text = (el.textContent || "").toLowerCase();
      if (rect.top < 70 || rect.top > 240 || rect.width < window.innerWidth * 0.45 || rect.height < 36 || rect.height > 130) {
        return false;
      }
      return text.indexOf("pi liaison") !== -1 || text.indexOf("ai-verde") !== -1;
    }) || null;
  }

  function installProjectBanner() {
    var title = getProjectTitle();
    var host = findControlRow();
    if (!host || !host.parentElement) return;

    var banner = document.querySelector(".scienceclaw-project-banner");
    if (!banner) {
      banner = document.createElement("section");
      banner.className = "scienceclaw-project-banner";
      banner.setAttribute("aria-label", "Current ScienceClaw working group");
      banner.innerHTML =
        '<div class="scienceclaw-project-banner__main">' +
        '<span class="scienceclaw-project-banner__eyebrow">Project</span>' +
        '<strong class="scienceclaw-project-banner__title"></strong>' +
        '<button class="scienceclaw-project-banner__edit" type="button" title="Edit project title" aria-label="Edit project title">Edit</button>' +
        '</div>' +
        '<span class="scienceclaw-project-banner__host"></span>';
      host.parentElement.insertBefore(banner, host.nextSibling);
    } else if (banner.previousElementSibling !== host) {
      host.parentElement.insertBefore(banner, host.nextSibling);
    }

    var titleEl = banner.querySelector(".scienceclaw-project-banner__title");
    var hostEl = banner.querySelector(".scienceclaw-project-banner__host");
    var editEl = banner.querySelector(".scienceclaw-project-banner__edit");
    if (titleEl) titleEl.textContent = title;
    if (hostEl) hostEl.textContent = window.location.host;
    if (!banner.dataset.scienceclawEditable) {
      banner.dataset.scienceclawEditable = "1";
      if (titleEl) {
        titleEl.setAttribute("role", "button");
        titleEl.setAttribute("tabindex", "0");
        titleEl.setAttribute("title", "Edit project title");
        titleEl.addEventListener("click", function () {
          startProjectTitleEdit(banner);
        });
        titleEl.addEventListener("keydown", function (event) {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            startProjectTitleEdit(banner);
          }
        });
      }
      if (editEl) {
        editEl.addEventListener("click", function (event) {
          event.preventDefault();
          startProjectTitleEdit(banner);
        });
      }
    }
    positionProjectBanner(host, banner);
  }

  function startProjectTitleEdit(banner) {
    var titleEl = banner.querySelector(".scienceclaw-project-banner__title");
    if (!titleEl || banner.querySelector(".scienceclaw-project-banner__input")) return;

    var input = document.createElement("input");
    input.className = "scienceclaw-project-banner__input";
    input.type = "text";
    input.value = getProjectTitle();
    input.setAttribute("aria-label", "Project title");

    titleEl.style.display = "none";
    titleEl.insertAdjacentElement("afterend", input);
    input.focus();
    input.select();

    var done = false;
    function finish(save) {
      if (done) return;
      done = true;
      if (save) titleEl.textContent = setProjectTitle(input.value);
      input.remove();
      titleEl.style.display = "";
    }

    input.addEventListener("keydown", function (event) {
      if (event.key === "Enter") finish(true);
      if (event.key === "Escape") finish(false);
    });
    input.addEventListener("blur", function () {
      finish(true);
    });
  }

  function positionProjectBanner(host, banner) {
    var rect = host.getBoundingClientRect();
    var left = Math.max(12, rect.left);
    var width = Math.min(720, rect.width, window.innerWidth - left - 24);
    var top = Math.min(184, Math.max(88, rect.bottom + 8));

    banner.style.setProperty("--scienceclaw-banner-top", Math.round(top) + "px");
    banner.style.setProperty("--scienceclaw-banner-left", Math.round(left) + "px");
    banner.style.setProperty("--scienceclaw-banner-width", Math.round(width) + "px");
  }

  function cleanSidebarBrand() {
    Array.prototype.forEach.call(document.querySelectorAll(".sidebar-brand"), function (brand) {
      Array.prototype.forEach.call(brand.querySelectorAll("*"), function (el) {
        if ((el.textContent || "").trim() === "Control") {
          el.classList.add("sidebar-brand__eyebrow");
        }
      });
    });
  }

  function applyBranding() {
    updateHead();
    updateAttributes();
    replaceExactText(document.body);
    installBrandPlate();
    installProjectBanner();
    cleanSidebarBrand();
    Array.prototype.forEach.call(document.querySelectorAll(".scienceclaw-oasis-mark"), function (el) {
      el.remove();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applyBranding);
  } else {
    applyBranding();
  }

  var pending = false;
  var observer = new MutationObserver(function () {
    if (pending) return;
    pending = true;
    window.setTimeout(function () {
      pending = false;
      applyBranding();
    }, 250);
  });
  observer.observe(document.documentElement, { childList: true, subtree: true });
  window.addEventListener("resize", applyBranding);
})();
