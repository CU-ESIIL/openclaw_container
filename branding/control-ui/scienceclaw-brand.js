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
    if (!isChatView()) {
      var existing = document.querySelector(".scienceclaw-brand-plate");
      if (existing) existing.remove();
      return;
    }
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
    if (!isChatView()) {
      var existing = document.querySelector(".scienceclaw-project-banner");
      if (existing) existing.remove();
      return;
    }
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

  function isChatView() {
    return window.location.pathname.indexOf("/chat") === 0;
  }

  function getCmsPort() {
    return (
      window.SCIENCECLAW_CONFIG && window.SCIENCECLAW_CONFIG.cmsPort ||
      window.SCIENCECLAW_CMS_PORT ||
      "8090"
    );
  }

  function getFilesUrl() {
    var protocol = window.location.protocol || "http:";
    var hostname = window.location.hostname || "127.0.0.1";
    return protocol + "//" + hostname + ":" + getCmsPort() + "/files?path=/workspace";
  }

  function getGithubUrl() {
    var protocol = window.location.protocol || "http:";
    var hostname = window.location.hostname || "127.0.0.1";
    return protocol + "//" + hostname + ":" + getCmsPort() + "/github";
  }

  function getCmsApiUrl(path) {
    var protocol = window.location.protocol || "http:";
    var hostname = window.location.hostname || "127.0.0.1";
    return protocol + "//" + hostname + ":" + getCmsPort() + path;
  }

  function escapeHtml(value) {
    return String(value || "").replace(/[&<>"']/g, function (ch) {
      return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[ch];
    });
  }

  function pathParent(path) {
    var clean = String(path || "/workspace").replace(/\/+$/, "") || "/";
    if (clean === "/") return "/";
    var idx = clean.lastIndexOf("/");
    return idx <= 0 ? "/" : clean.slice(0, idx);
  }

  function shortPath(path) {
    var value = String(path || "/workspace");
    return value.replace(/^\/workspace/, "workspace") || "/";
  }

  function fileUrl(path) {
    var protocol = window.location.protocol || "http:";
    var hostname = window.location.hostname || "127.0.0.1";
    return protocol + "//" + hostname + ":" + getCmsPort() + "/files?path=" + encodeURIComponent(path || "/workspace");
  }

  function githubRepoUrl(owner, repo) {
    return getGithubUrl() + "?repo=" + encodeURIComponent(owner + "/" + repo);
  }

  function agentPath(path) {
    return String(path || "").replace(/^\/data\/workspace/, "/workspace") || "/workspace/repos";
  }

  function postCms(path, fields) {
    var body = new URLSearchParams();
    Object.keys(fields || {}).forEach(function (key) {
      body.set(key, fields[key]);
    });
    return fetch(getCmsApiUrl(path), {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: body.toString(),
    });
  }

  function closeWorkspacePanels(wrapper) {
    Array.prototype.forEach.call(wrapper.querySelectorAll(".scienceclaw-sidebar-panel"), function (panel) {
      panel.hidden = true;
    });
  }

  function toggleWorkspacePanel(wrapper, name) {
    var panel = wrapper.querySelector('[data-scienceclaw-panel-body="' + name + '"]');
    if (!panel) return;
    var opening = panel.hidden;
    closeWorkspacePanels(wrapper);
    panel.hidden = !opening;
    if (opening) loadWorkspacePanel(name, panel);
  }

  function renderPanelError(panel, message, href) {
    panel.innerHTML =
      '<p class="scienceclaw-sidebar-muted">' + escapeHtml(message) + '</p>' +
      '<a class="scienceclaw-sidebar-link" href="' + href + '" target="_blank" rel="noopener">Open full page</a>';
  }

  function loadWorkspacePanel(name, panel) {
    if (name === "files") loadFilesPanel(panel);
    if (name === "github") loadGithubPanel(panel);
  }

  function loadFilesPanel(panel) {
    var currentPath = panel.dataset.scienceclawPath || "/workspace";
    panel.innerHTML = '<p class="scienceclaw-sidebar-muted">Loading ' + escapeHtml(shortPath(currentPath)) + '...</p>';
    fetch(getCmsApiUrl("/api/file/list?path=" + encodeURIComponent(currentPath)))
      .then(function (response) {
        if (!response.ok) throw new Error("File manager unavailable");
        return response.json();
      })
      .then(function (data) {
        panel.dataset.scienceclawPath = data.path || currentPath;
        var entries = (data.entries || []).slice(0, 80);
        var rows = entries.map(function (entry) {
          var isFolder = entry.kind === "folder";
          var icon = isFolder ? "▸" : "·";
          var label = isFolder ? "dir" : entry.kind;
          var action = isFolder
            ? '<button class="scienceclaw-file-row" type="button" data-path="' + escapeHtml(entry.path) + '">'
            : '<a class="scienceclaw-file-row" href="' + fileUrl(entry.path) + '" target="_blank" rel="noopener">';
          var close = isFolder ? "</button>" : "</a>";
          return '<li>' + action +
            '<span class="scienceclaw-file-row__icon">' + icon + '</span>' +
            '<span class="scienceclaw-file-row__name">' + escapeHtml(entry.name) + '</span>' +
            '<small>' + escapeHtml(label) + '</small>' +
            close + '</li>';
        }).join("");
        panel.innerHTML =
          '<div class="scienceclaw-sidebar-navhead">' +
          '<strong>' + escapeHtml(shortPath(data.path || currentPath)) + '</strong>' +
          '<div>' +
          '<button class="scienceclaw-sidebar-mini" type="button" data-file-action="up">Up</button>' +
          '<button class="scienceclaw-sidebar-mini" type="button" data-file-action="refresh">Refresh</button>' +
          '</div>' +
          '</div>' +
          '<ul class="scienceclaw-file-list">' + (rows || '<li><span class="scienceclaw-sidebar-muted">No files yet</span></li>') + '</ul>' +
          '<a class="scienceclaw-sidebar-link" href="' + fileUrl(data.path || currentPath) + '" target="_blank" rel="noopener">Open full file manager</a>';
        Array.prototype.forEach.call(panel.querySelectorAll(".scienceclaw-file-row[data-path]"), function (button) {
          button.addEventListener("click", function () {
            panel.dataset.scienceclawPath = button.getAttribute("data-path") || "/workspace";
            loadFilesPanel(panel);
          });
        });
        panel.querySelector('[data-file-action="up"]').addEventListener("click", function () {
          panel.dataset.scienceclawPath = pathParent(panel.dataset.scienceclawPath || "/workspace");
          loadFilesPanel(panel);
        });
        panel.querySelector('[data-file-action="refresh"]').addEventListener("click", function () {
          loadFilesPanel(panel);
        });
      })
      .catch(function (error) {
        renderPanelError(panel, "Could not load the file navigator here. " + (error && error.message ? error.message : ""), fileUrl(currentPath));
      });
  }

  function loadGithubPanel(panel) {
    panel.innerHTML = '<p class="scienceclaw-sidebar-muted">Checking GitHub status...</p>';
    Promise.all([
      fetch(getCmsApiUrl("/api/github/status")).then(function (response) {
        if (!response.ok) throw new Error("GitHub status unavailable");
        return response.json();
      }),
      fetch(getCmsApiUrl("/api/github/repos")).then(function (response) {
        if (!response.ok) throw new Error("GitHub registry unavailable");
        return response.json();
      }),
    ])
      .then(function (response) {
        var data = response[0];
        var registry = response[1];
        var state = data.authenticated ? "Authenticated" : "Not authenticated";
        var token = data.token_available ? "token visible" : "no token";
        var repos = registry.repositories || [];
        var repoRows = repos.map(function (repo) {
          var name = repo.owner + "/" + repo.repo;
          var cloned = repo.cloned ? "cloned" : "not cloned";
          var branch = repo.current_branch || repo.default_branch || "";
          var safeBranch = branch && ["main", "master"].indexOf(branch) === -1;
          var contribute = repo.permission_tier === "contribute";
          var actions = repo.cloned
            ? '<button type="button" data-gh-action="fetch" data-owner="' + escapeHtml(repo.owner) + '" data-repo="' + escapeHtml(repo.repo) + '">Fetch</button>' +
              '<button type="button" data-gh-action="pull" data-owner="' + escapeHtml(repo.owner) + '" data-repo="' + escapeHtml(repo.repo) + '">Pull latest</button>' +
              (contribute && safeBranch ? '<button type="button" data-gh-action="push" data-owner="' + escapeHtml(repo.owner) + '" data-repo="' + escapeHtml(repo.repo) + '">Push branch</button>' : '')
            : '<button type="button" data-gh-action="clone" data-owner="' + escapeHtml(repo.owner) + '" data-repo="' + escapeHtml(repo.repo) + '">Clone</button>';
          return '<li class="scienceclaw-repo-row">' +
            '<a href="' + githubRepoUrl(repo.owner, repo.repo) + '" target="_blank" rel="noopener"><strong>' + escapeHtml(name) + '</strong></a>' +
            '<small>' + escapeHtml(repo.permission_tier || "read") + " · " + escapeHtml(cloned) + " · " + escapeHtml(branch) + '</small>' +
            '<code>' + escapeHtml(agentPath(repo.local_path)) + '</code>' +
            '<div class="scienceclaw-repo-actions">' + actions + '</div>' +
            '</li>';
        }).join("");
        panel.innerHTML =
          '<div class="scienceclaw-shared-state">' +
          '<strong>Shared with agents</strong>' +
          '<code>/workspace/.openclaw-github/authorized-repos.yaml</code>' +
          '<code>/workspace/repos/</code>' +
          '</div>' +
          '<div class="scienceclaw-sidebar-status">' +
          '<strong>' + escapeHtml(state) + '</strong>' +
          '<small>' + escapeHtml(data.auth_method || "none") + " · " + escapeHtml(token) + '</small>' +
          '</div>' +
          '<button class="scienceclaw-sidebar-action" type="button" data-gh-action="setup">Configure git credentials</button>' +
          '<form class="scienceclaw-repo-form">' +
          '<label>Add repo agents can see</label>' +
          '<input name="owner" placeholder="owner" required>' +
          '<input name="repo" placeholder="repo" required>' +
          '<input name="url" placeholder="optional github.com URL">' +
          '<select name="permission_tier"><option value="read">read</option><option value="contribute">contribute</option></select>' +
          '<button type="submit">Add repo</button>' +
          '</form>' +
          '<ul class="scienceclaw-repo-list">' + (repoRows || '<li class="scienceclaw-sidebar-muted">No authorized repositories yet.</li>') + '</ul>' +
          '<a class="scienceclaw-sidebar-link" href="' + getGithubUrl() + '" target="_blank" rel="noopener">Open full GitHub manager</a>';
        panel.querySelector('[data-gh-action="setup"]').addEventListener("click", function (event) {
          event.currentTarget.textContent = "Configuring...";
          postCms("/api/github/setup-git", {})
            .then(function () { loadGithubPanel(panel); })
            .catch(function () { renderPanelError(panel, "Git credential setup could not run here.", getGithubUrl()); });
        });
        panel.querySelector(".scienceclaw-repo-form").addEventListener("submit", function (event) {
          event.preventDefault();
          var form = event.currentTarget;
          postCms("/api/github/repos", {
            owner: form.owner.value,
            repo: form.repo.value,
            url: form.url.value,
            permission_tier: form.permission_tier.value,
          }).then(function () {
            form.reset();
            loadGithubPanel(panel);
          }).catch(function () {
            renderPanelError(panel, "Could not add the repository here.", getGithubUrl());
          });
        });
        Array.prototype.forEach.call(panel.querySelectorAll("[data-gh-action][data-owner]"), function (button) {
          button.addEventListener("click", function () {
            var action = button.getAttribute("data-gh-action");
            var owner = button.getAttribute("data-owner");
            var repo = button.getAttribute("data-repo");
            button.textContent = action + "...";
            postCms("/api/github/repos/" + encodeURIComponent(owner) + "/" + encodeURIComponent(repo) + "/" + action, {})
              .then(function () { loadGithubPanel(panel); })
              .catch(function () { renderPanelError(panel, "GitHub action failed here. Open the full manager for details.", githubRepoUrl(owner, repo)); });
          });
        });
      })
      .catch(function (error) {
        renderPanelError(panel, "Could not load GitHub manager here. " + (error && error.message ? error.message : ""), getGithubUrl());
      });
  }

  function installWorkspaceLinks() {
    var sidebarTargets = Array.prototype.slice.call(document.querySelectorAll("aside, nav, [class*=sidebar]"));
    var host = sidebarTargets.find(function (el) {
      var rect = el.getBoundingClientRect();
      return rect.width > 120 && rect.width < 520 && rect.height > 240;
    });
    if (!host) return;

    var wrapper = document.querySelector(".scienceclaw-workspace-links");
    if (!wrapper) {
      wrapper = document.createElement("div");
      wrapper.className = "scienceclaw-workspace-links";
      host.appendChild(wrapper);
    }
    if (wrapper.dataset.scienceclawReady) return;
    wrapper.dataset.scienceclawReady = "1";
    wrapper.innerHTML =
      '<button class="scienceclaw-sidebar-tool" type="button" data-scienceclaw-panel="files">' +
      '<span class="scienceclaw-sidebar-tool__icon" aria-hidden="true">▣</span>' +
      '<span><strong>Files</strong><small>Browse workspace and outputs</small></span>' +
      '</button>' +
      '<section class="scienceclaw-sidebar-panel" data-scienceclaw-panel-body="files" hidden></section>' +
      '<button class="scienceclaw-sidebar-tool" type="button" data-scienceclaw-panel="github">' +
      '<span class="scienceclaw-sidebar-tool__icon" aria-hidden="true">⌁</span>' +
      '<span><strong>GitHub Auth</strong><small>Credentials, repos, branches, PRs</small></span>' +
      '</button>' +
      '<section class="scienceclaw-sidebar-panel" data-scienceclaw-panel-body="github" hidden></section>';
    wrapper.querySelector('[data-scienceclaw-panel="files"]').addEventListener("click", function () {
      toggleWorkspacePanel(wrapper, "files");
    });
    wrapper.querySelector('[data-scienceclaw-panel="github"]').addEventListener("click", function () {
      toggleWorkspacePanel(wrapper, "github");
    });
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

  function hideUnsupportedUpdateBanners() {
    var needles = [
      "Update available:",
      "managed-service-handoff-unavailable",
    ];
    Array.prototype.forEach.call(document.querySelectorAll("button, div, section, aside"), function (el) {
      if (el.classList.contains("scienceclaw-hidden-updater")) return;
      var text = (el.textContent || "").replace(/\s+/g, " ").trim();
      if (!text) return;
      var matches = needles.some(function (needle) {
        return text.indexOf(needle) !== -1;
      });
      if (!matches) return;

      var rect = el.getBoundingClientRect();
      if (rect.top > 260 || rect.width < 260 || rect.height < 32 || rect.height > 180) return;
      if (el.querySelector(".scienceclaw-brand-plate, .scienceclaw-project-banner")) return;

      el.classList.add("scienceclaw-hidden-updater");
      el.setAttribute("aria-hidden", "true");
    });
  }

  function applyBranding() {
    updateHead();
    updateAttributes();
    replaceExactText(document.body);
    hideUnsupportedUpdateBanners();
    installBrandPlate();
    installProjectBanner();
    installWorkspaceLinks();
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
