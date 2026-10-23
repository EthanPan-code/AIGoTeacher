"""CustomTkinter browser for KataGo Training API models."""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Callable

import customtkinter as ctk

from services.katago_model_manager import (
    KataGoModel,
    KataGoModelError,
    KataGoModelManager,
    KataGoModelPage,
    DownloadProgress,
)


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
        self.page: KataGoModelPage | None = None
        self._closed = False
        self._page_loading = False
        self._row_widgets: list[ctk.CTkFrame] = []
        self._download_model: KataGoModel | None = None
        self._download_path: Path | None = None

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

        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 8))
        self.tab_view.add(self.translate("tab.katago_models"))
        self.tab_view.set(self.translate("tab.katago_models"))
        model_tab = self.tab_view.tab(self.translate("tab.katago_models"))
        model_tab.grid_columnconfigure(0, weight=1)

        self.list_frame = ctk.CTkScrollableFrame(
            model_tab,
            label_text=self.translate("label.katago_model_list"),
        )
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 8))
        self.list_frame.grid_columnconfigure(0, weight=1)

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=3, column=0, sticky="ew", padx=18, pady=(0, 18))
        footer.grid_columnconfigure(1, weight=1)
        self.previous_button = ctk.CTkButton(
            footer,
            text=self.translate("button.previous"),
            width=110,
            command=self.previous_page,
        )
        self.previous_button.grid(row=0, column=0, sticky="w")
        self.page_label = ctk.CTkLabel(footer, text="", anchor="center")
        self.page_label.grid(row=0, column=1, sticky="ew", padx=12)
        self.next_button = ctk.CTkButton(
            footer,
            text=self.translate("button.next"),
            width=110,
            command=self.next_page,
        )
        self.next_button.grid(row=0, column=2, sticky="e")

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
        self._load_page(self.page.url if self.page else None)

    def next_page(self) -> None:
        if self.page and self.page.next_url:
            self._load_page(self.page.next_url)

    def previous_page(self) -> None:
        if self.page and self.page.previous_url:
            self._load_page(self.page.previous_url)

    def _load_page(self, url: str | None) -> None:
        if self._page_loading:
            return
        self._page_loading = True
        self.refresh_button.configure(state="disabled")
        self.status_label.configure(text=self.translate("status.katago_models_loading"))
        threading.Thread(
            target=self._load_page_worker,
            args=(url,),
            daemon=True,
        ).start()

    def _load_page_worker(self, url: str | None) -> None:
        try:
            page = self.manager.fetch_page(url) if url else self.manager.fetch_page()
        except Exception as exc:
            self._run_on_ui(self._show_page_error, exc)
            return
        self._run_on_ui(self._show_page, page)

    def _show_page(self, page: KataGoModelPage) -> None:
        self._page_loading = False
        self.page = page
        self.refresh_button.configure(state="normal")
        self.status_label.configure(
            text=self.translate("status.katago_models_count", count=page.count)
        )
        self.page_label.configure(
            text=self.translate(
                "status.katago_models_page",
                current=self._page_number(page.url),
                total=max(1, (page.count + len(page.results) - 1) // max(1, len(page.results))),
            )
        )
        self.previous_button.configure(
            state="normal" if page.previous_url else "disabled"
        )
        self.next_button.configure(state="normal" if page.next_url else "disabled")
        self._render_models(page.results)

    def _show_page_error(self, error: Exception) -> None:
        self._page_loading = False
        self.refresh_button.configure(state="normal")
        self.status_label.configure(
            text=self.translate("status.katago_models_error", error=str(error))
        )

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
                font=("Segoe UI", 13, "bold"),
                anchor="w",
            ).grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 2))
            details = self.translate(
                "status.katago_model_details",
                network_size=model.network_size,
                size=self._format_bytes(model.model_file_bytes),
                created=model.created_at[:10],
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
        self.manager.cancel_download()
        self.destroy()

    def _run_on_ui(self, callback, *args) -> None:
        if not self._closed and self.winfo_exists():
            self.after(0, callback, *args)

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
        self.browser = KataGoModelBrowserFrame(
            self,
            manager,
            translator=translator,
            on_apply=on_apply,
        )
        self.browser.grid(row=0, column=0, sticky="nsew")
        self.protocol("WM_DELETE_WINDOW", self._close)
        self.transient(master)
        self.grab_set()

    def _close(self) -> None:
        self.browser.close()
        self.grab_release()
        self.destroy()
