"""CustomTkinter browser for KataGo Training API models."""

from __future__ import annotations

import threading, sys, os
from pathlib import Path
from typing import Callable

import customtkinter as ctk

from services.katago_model_manager import (
    KataGoModel,
    KataGoModelHTTPError,
    KataGoModelManager,
    KataGoModelNetworkError,
    DownloadProgress,
)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    # ✅ exe 模式（onedir）
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), relative_path)

    # 開發模式
    return os.path.join(os.path.abspath('.'), relative_path)

class KataGoModelBrowserFrame(ctk.CTkFrame):
    """Browse, download, and apply KataGo neural-network models."""

    def __init__(
        self,
        master,
        manager: KataGoModelManager,
        *,
        translator: Callable[..., str],
        on_apply: Callable[[KataGoModel, Path], None] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)
        self.manager = manager
        self.translate = translator
        self.on_apply = on_apply
        self.models: tuple[KataGoModel, ...] = ()
        self._closed = False
        self._models_loading = False
        self._row_widgets: list[ctk.CTkFrame] = []
        self._download_model: KataGoModel | None = None
        self._download_path: Path | None = None
        self._filtered_models: tuple[KataGoModel, ...] = ()
        self._local_page = 0
        self._local_page_size = 50
        self._search_after_id = None
        self._ui_generation = 0
        self.search_var = ctk.StringVar(value="")
        self.category_var = ctk.StringVar(value="")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self._build_widgets()
        self.refresh()

    def _build_widgets(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 8))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header,
            text=self.translate("dialog.katago_online_models_title"),
            font=("Segoe UI", 20, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="w")
        self.status_label = ctk.CTkLabel(header, text="", anchor="w")
        self.status_label.grid(row=1, column=0, sticky="w", pady=(4, 0))
        self.refresh_button = ctk.CTkButton(
            header,
            text=self.translate("button.refresh"),
            width=110,
            command=self.refresh,
        )
        self.refresh_button.grid(row=0, column=1, rowspan=2, padx=(12, 0))

        filters = ctk.CTkFrame(self, fg_color="transparent")
        filters.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 8))
        filters.grid_columnconfigure(0, weight=1)
        self.search_entry = ctk.CTkEntry(
            filters,
            textvariable=self.search_var,
            placeholder_text=self.translate("placeholder.katago_model_search"),
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.search_entry.bind("<KeyRelease>", lambda _event: self._schedule_search())
        self.category_menu = ctk.CTkOptionMenu(
            filters,
            variable=self.category_var,
            values=[self.translate("filter.all_models")],
            command=lambda _value: self._render_filtered_models(reset_page=True),
            width=190,
        )
        self.category_menu.grid(row=0, column=1, sticky="e")

        self.list_frame = ctk.CTkScrollableFrame(
            self,
            label_text=self.translate("label.katago_model_list"),
        )
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 8))
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.local_pagination = ctk.CTkFrame(self, fg_color="transparent")
        self.local_pagination.grid(row=3, column=0, sticky="ew", padx=18, pady=(0, 4))
        self.local_pagination.grid_columnconfigure(1, weight=1)
        self.local_previous_button = ctk.CTkButton(
            self.local_pagination,
            text=self.translate("button.previous"),
            width=100,
            command=self._previous_local_page,
        )
        self.local_previous_button.grid(row=0, column=0, sticky="w")
        self.local_page_label = ctk.CTkLabel(self.local_pagination, text="", anchor="center")
        self.local_page_label.grid(row=0, column=1, sticky="ew", padx=10)
        self.local_next_button = ctk.CTkButton(
            self.local_pagination,
            text=self.translate("button.next"),
            width=100,
            command=self._next_local_page,
        )
        self.local_next_button.grid(row=0, column=2, sticky="e")

        self.download_status = ctk.CTkLabel(self, text="", anchor="w")
        self.download_status.grid(row=4, column=0, sticky="ew", padx=18)
        self.progress_bar = ctk.CTkProgressBar(self, height=8)
        self.progress_bar.grid(row=5, column=0, sticky="ew", padx=18, pady=(4, 0))
        self.progress_bar.set(0)
        self.cancel_button = ctk.CTkButton(
            self,
            text=self.translate("button.cancel"),
            width=110,
            command=self.cancel_download,
        )
        self.cancel_button.grid(row=6, column=0, sticky="e", padx=18, pady=(6, 12))
        self.cancel_button.grid_remove()
        self.apply_button = ctk.CTkButton(
            self,
            text=self.translate("button.apply_model"),
            width=130,
            command=self.apply_downloaded_model,
        )
        self.apply_button.grid(row=6, column=0, sticky="w", padx=18, pady=(6, 12))
        self.apply_button.grid_remove()

    def refresh(self) -> None:
        if self._models_loading:
            return
        self._models_loading = True
        self.refresh_button.configure(state="disabled")
        self.status_label.configure(text=self.translate("status.katago_models_loading"))
        cached_models = self.manager.load_cached_models()
        if cached_models:
            # The catalog is local and cheap to read: show it before the
            # network validation request completes.
            self._show_models(cached_models, reset_page=True, loading_complete=False)
        threading.Thread(
            target=self._load_models_worker,
            args=(cached_models,),
            daemon=True,
        ).start()

    def _load_models_worker(self, cached_models: tuple[KataGoModel, ...]) -> None:
        try:
            models = self.manager.fetch_models_incremental(
                cached_models,
                on_batch=lambda batch, _count: self._run_on_ui(
                    self._show_models,
                    batch,
                    False,
                    False,
                ),
            )
        except Exception as exc:
            self._run_on_ui(self._show_models_error, exc)
            return
        self._run_on_ui(self._show_models, models, False, True)

    def _show_models(
        self,
        models: tuple[KataGoModel, ...],
        reset_page: bool = False,
        loading_complete: bool = True,
    ) -> None:
        self.models = models
        if loading_complete:
            self._models_loading = False
            self.refresh_button.configure(state="normal")
        self.status_label.configure(
            text=self.translate("status.katago_models_count", count=len(models))
        )
        categories = sorted({model.network_size for model in models})
        all_label = self.translate("filter.all_models")
        self.category_menu.configure(values=[all_label, *categories])
        if self.category_var.get() not in {all_label, *categories}:
            self.category_var.set(all_label)
        self._render_filtered_models(reset_page=reset_page)

    def _show_models_error(self, error: Exception) -> None:
        self._models_loading = False
        self.refresh_button.configure(state="normal")
        if isinstance(error, KataGoModelNetworkError):
            message_key = "status.katago_model_network_error"
        elif isinstance(error, KataGoModelHTTPError):
            message_key = "status.katago_model_http_error"
        else:
            message_key = "status.katago_models_error"
        self.status_label.configure(
            text=self.translate(message_key)
        )

    def _schedule_search(self) -> None:
        if self._search_after_id is not None:
            try:
                self.after_cancel(self._search_after_id)
            except (RuntimeError, Exception):
                pass
        self._search_after_id = self.after(180, self._apply_scheduled_search)

    def _apply_scheduled_search(self) -> None:
        self._search_after_id = None
        self._render_filtered_models(reset_page=True)

    def _render_filtered_models(self, *, reset_page: bool = False) -> None:
        if reset_page:
            self._local_page = 0
        query = self.search_var.get().strip().lower()
        all_label = self.translate("filter.all_models")
        category = self.category_var.get() or all_label
        self._filtered_models = tuple(
            model
            for model in self.models
            if (category == all_label or model.network_size == category)
            and (
                not query
                or query in model.name.lower()
                or query in model.network_size.lower()
                or query in model.notes.lower()
            )
        )
        page_start = self._local_page * self._local_page_size
        page_end = page_start + self._local_page_size
        self._render_models(self._filtered_models[page_start:page_end])
        total_pages = max(1, (len(self._filtered_models) + self._local_page_size - 1) // self._local_page_size)
        self.local_page_label.configure(
            text=self.translate(
                "status.katago_models_page",
                current=self._local_page + 1,
                total=total_pages,
            )
        )
        self.local_previous_button.configure(
            state="normal" if self._local_page > 0 else "disabled"
        )
        self.local_next_button.configure(
            state="normal" if self._local_page + 1 < total_pages else "disabled"
        )
        if not self._filtered_models and self.models:
            self.download_status.configure(text=self.translate("status.katago_models_no_match"))

    def _previous_local_page(self) -> None:
        if self._local_page > 0:
            self._local_page -= 1
            self._render_filtered_models()

    def _next_local_page(self) -> None:
        if (self._local_page + 1) * self._local_page_size < len(self._filtered_models):
            self._local_page += 1
            self._render_filtered_models()

    def _render_models(self, models: tuple[KataGoModel, ...]) -> None:
        for widget in self._row_widgets:
            widget.destroy()
        self._row_widgets.clear()
        for row, model in enumerate(models):
            frame = ctk.CTkFrame(self.list_frame, fg_color=("#f4eee4", "#252525"))
            frame.grid(row=row, column=0, sticky="ew", padx=4, pady=4)
            frame.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                frame,
                text=model.name,
                font=("Microsoft JhengHei", 13, "bold"),
                anchor="w",
            ).grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 2))
            date = model.created_at[:10]
            # 民國紀年
            # date = date.split("-")
            # date[0] = str(int(date[0])-1911)
            # date = "-".join(date)
            details = self.translate(
                "status.katago_model_details",
                network_size=model.network_size,
                size=self._format_bytes(model.model_file_bytes),
                created=date,
            )
            ctk.CTkLabel(frame, text=details, anchor="w").grid(
                row=1, column=0, sticky="ew", padx=12, pady=(0, 8)
            )
            action = ctk.CTkButton(
                frame,
                text=self.translate("button.download"),
                width=110,
                command=lambda item=model: self.start_download(item),
            )
            action.grid(row=0, column=1, rowspan=2, padx=12, pady=10)
            self._row_widgets.append(frame)

    def start_download(self, model: KataGoModel) -> None:
        if self.manager.is_downloading:
            return
        self._download_model = model
        self._download_path = None
        self.apply_button.grid_remove()
        self.download_status.configure(
            text=self.translate("status.katago_model_downloading", name=model.name)
        )
        self.progress_bar.set(0)
        self.cancel_button.grid()
        threading.Thread(
            target=self._download_worker,
            args=(model,),
            daemon=True,
        ).start()

    def _download_worker(self, model: KataGoModel) -> None:
        try:
            path = self.manager.download_model(
                model,
                progress_callback=lambda progress: self._run_on_ui(
                    self._show_progress, progress
                ),
            )
        except Exception as exc:
            self._run_on_ui(self._show_download_error, exc)
            return
        self._run_on_ui(self._show_download_complete, model, path)

    def _show_progress(self, progress: DownloadProgress) -> None:
        self.progress_bar.set(progress.fraction)
        self.download_status.configure(
            text=self.translate(
                "status.katago_model_progress",
                downloaded=self._format_bytes(progress.downloaded_bytes),
                total=self._format_bytes(progress.total_bytes),
            )
        )

    def _show_download_complete(self, model: KataGoModel, path: Path) -> None:
        self._download_path = path
        self.cancel_button.grid_remove()
        self.apply_button.grid()
        self.download_status.configure(
            text=self.translate("status.katago_model_ready", name=model.name)
        )

    def _show_download_error(self, error: Exception) -> None:
        self.cancel_button.grid_remove()
        if isinstance(error, KataGoModelNetworkError):
            self.download_status.configure(
                text=self.translate("status.katago_model_network_error")
            )
            return
        if isinstance(error, KataGoModelHTTPError):
            self.download_status.configure(
                text=self.translate("status.katago_model_http_error")
            )
            return
        self.download_status.configure(
            text=self.translate("status.katago_model_download_error", error=str(error))
        )

    def cancel_download(self) -> None:
        self.manager.cancel_download()
        self.download_status.configure(text=self.translate("status.katago_model_cancelling"))

    def apply_downloaded_model(self) -> None:
        if self._download_model and self._download_path and self.on_apply:
            self.on_apply(self._download_model, self._download_path)

    def close(self) -> None:
        self._closed = True
        self._ui_generation += 1
        if self._search_after_id is not None:
            try:
                self.after_cancel(self._search_after_id)
            except (RuntimeError, Exception):
                pass
            self._search_after_id = None
        self.manager.cancel_download()
        self.destroy()

    def _run_on_ui(self, callback, *args) -> None:
        if self._closed:
            return
        generation = self._ui_generation
        try:
            self.after(0, self._invoke_if_alive, generation, callback, args)
        except Exception:
            return

    def _invoke_if_alive(self, generation, callback, args) -> None:
        if self._closed or generation != self._ui_generation or not self.winfo_exists():
            return
        callback(*args)

    @staticmethod
    def _format_bytes(value: int) -> str:
        size = float(value)
        for unit in ("B", "KB", "MB", "GB"):
            if size < 1024 or unit == "GB":
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{value} B"

    @staticmethod
    def _page_number(url: str) -> int:
        marker = "page="
        if marker in url:
            try:
                return int(url.split(marker, 1)[1].split("&", 1)[0])
            except ValueError:
                pass
        return 1


class KataGoModelBrowserWindow(ctk.CTkToplevel):
    """Window wrapper for the online model browser frame."""

    def __init__(self, master, manager, *, translator, on_apply=None):
        super().__init__(master)
        self.title(translator("dialog.katago_online_models_title"))
        self.geometry("920x680")
        self.minsize(760, 520)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.iconbitmap(resource_path("image/logo/logo.ico"))
        self.browser = KataGoModelBrowserFrame(
            self,
            manager,
            translator=translator,
            on_apply=on_apply,
        )
        self.browser.grid(row=0, column=0, sticky="nsew")
        self.protocol("WM_DELETE_WINDOW", self._close)
        self.grab_set()

    def _close(self) -> None:
        self.browser.close()
        self.grab_release()
        self.destroy()
