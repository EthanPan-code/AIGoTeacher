import threading
from typing import Dict, Optional, Callable

from opencc import OpenCC

from .base import LLMProvider


OLLAMA_MODELS = ["qwen2.5:1.5b", "llama3.2:1b", "gemma2:2b", "qwen2.5:3b", "qwen2.5:7b"]


class OllamaProvider(LLMProvider):
    def __init__(self, ui_callback, status_callback=None, model_name="qwen2.5:1.5b", translator=None, language_getter=None, on_complete_callback=None):
        super().__init__(ui_callback, status_callback, translator, language_getter, on_complete_callback)
        self.model_name = model_name
        self.cc = OpenCC("s2twp")

    def get_available_models(self):
        return OLLAMA_MODELS

    def validate_config(self):
        try:
            import ollama  # noqa: F401
            return (True, None)
        except Exception as e:
            return (False, f"Ollama 驗證失敗: {str(e)}")

    def set_model(self, model_name):
        self.model_name = model_name
        if self.status_callback:
            self.status_callback(self.tr("status.ollama_model_changed", model=model_name))

    def get_local_models(self):
        """
        獲取本地已下載的 Ollama 模型集合
        
        Returns:
            set: 模型名稱集合
        """
        from services.ollama_manager import get_ollama_manager
        manager = get_ollama_manager()
        return manager.get_local_models()

    def get_model_status(self) -> Dict[str, str]:
        """
        獲取所有可用 Ollama 模型的狀態
        
        Returns:
            Dict[str, str]: 模型狀態映射，例如 {'qwen2.5:1.5b': 'available', 'llama3.2:1b': 'pending'}
        """
        from services.ollama_manager import get_ollama_manager
        manager = get_ollama_manager()
        return manager.get_model_status(OLLAMA_MODELS)

    def is_model_available(self, model_name: str) -> bool:
        """
        檢查指定模型是否已下載
        
        Args:
            model_name (str): 模型名稱
        
        Returns:
            bool: True 如果模型已下載
        """
        from services.ollama_manager import get_ollama_manager
        manager = get_ollama_manager()
        return manager.is_model_available(model_name)

    def get_model_size(self, model_name: str) -> Optional[str]:
        """
        獲取模型大小信息
        
        Args:
            model_name (str): 模型名稱
        
        Returns:
            Optional[str]: 模型大小字符串，例如 '3.8 GB'
        """
        from services.ollama_manager import get_ollama_manager
        manager = get_ollama_manager()
        return manager.get_model_size(model_name)

    def start_model_download(
        self,
        model_name: str,
        progress_callback: Optional[Callable[[str], None]] = None,
        complete_callback: Optional[Callable[[bool, str], None]] = None
    ) -> bool:
        """
        開始異步下載 Ollama 模型
        
        Args:
            model_name (str): 要下載的模型名稱
            progress_callback (Optional[Callable]): 進度回調函數，簽名: callback(status_text)
            complete_callback (Optional[Callable]): 完成回調函數，簽名: callback(success, message)
        
        Returns:
            bool: True 如果成功啟動下載，False 如果已有下載進行中
        """
        from services.ollama_manager import get_ollama_manager
        manager = get_ollama_manager()
        return manager.pull_model_async(model_name, progress_callback, complete_callback)

    def is_downloading(self) -> bool:
        """檢查是否有模型正在下載"""
        from services.ollama_manager import get_ollama_manager
        manager = get_ollama_manager()
        return manager.downloading

    def start_commentary(self, critical_data):
        if self.is_generating:
            return

        self.is_generating = True
        self.ui_callback(critical_data.get("thinking_text", self.tr("teacher.thinking")))
        threading.Thread(target=self._generate_task, args=(critical_data,), daemon=True).start()

    def _generate_task(self, data):
        try:
            import ollama

            prompt = data.get("user_prompt")
            system_prompt = data.get("system_prompt", self.tr("teacher.system_prompt"))
            if prompt is None:
                turn = data["turn"]
                user_move = data["user_move"]
                winrate_drop = data["winrate_drop"] * 100
                best_move = data["current_best_moves"][0]["move"] if data["current_best_moves"] else self.tr("teacher.best_unknown")
                prompt = self.tr(
                    "teacher.user_prompt",
                    turn=turn,
                    user_move=user_move,
                    winrate_drop=winrate_drop,
                    best_move=best_move,
                )
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                stream=True,
            )

            full_content = ""
            for chunk in response:
                if "message" in chunk and "content" in chunk["message"]:
                    part = chunk["message"]["content"]
                    full_content += part
                    converted_text = self.cc.convert(full_content) if self.language_getter() == "zh_TW" else full_content
                    self.ui_callback(converted_text)

        except Exception as e:
            print(f"Ollama 發生錯誤: {e}")
            self.ui_callback(self._fallback_commentary(data, e))
            if self.status_callback:
                self.status_callback(self.tr("status.ollama_fallback"))
        finally:
            self.is_generating = False
            # 【Phase 1】生成完成 — 呼叫完成回呼
            if self.on_complete_callback:
                try:
                    self.on_complete_callback()
                except Exception as e:
                    print(f"完成回呼執行失敗: {e}")

    def _fallback_commentary(self, data, error):
        if data.get("fallback_text"):
            return data["fallback_text"]

        turn = data.get("turn", "?")
        user_move = data.get("user_move", "?")
        winrate_drop = data.get("winrate_drop", 0) * 100
        best_move = self.tr("teacher.best_unknown")
        best_moves = data.get("current_best_moves") or []
        if best_moves:
            best_move = best_moves[0].get("move", self.tr("teacher.best_unknown"))

        error_text = str(error)
        if "requires more system memory" in error_text:
            hint = self.tr("teacher.memory_hint")
        elif "model" in error_text.lower() and ("not found" in error_text.lower() or "pull" in error_text.lower()):
            hint = self.tr("teacher.model_not_found_hint", model=self.model_name)
        else:
            hint = self.tr("teacher.generic_error_hint", error=error_text)

        return self.tr(
            "teacher.fallback",
            turn=turn,
            user_move=user_move,
            winrate_drop=winrate_drop,
            best_move=best_move,
            hint=hint,
        )
