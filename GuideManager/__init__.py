"""Guide management module."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class GuideNotFoundError(FileNotFoundError):
    """Raised when the requested guide file cannot be found."""


DEFAULT_8D_GUIDE: Dict[str, Any] = {
    "method": "8D",
    "description": (
        "8D (Eight Disciplines) metodu, ürün ve süreç kaynaklı problemleri "
        "sistematik şekilde çözmek için geliştirilmiş etkili bir problem "
        "çözme tekniğidir. Özellikle otomotiv ve üretim sektöründe yaygındır."
    ),
    "steps": [
        {
            "step": "D1",
            "title": "Ekip Oluşturma",
            "detail": (
                "Problemi analiz etmek ve çözmek için farklı disiplinlerden, "
                "konuyla ilgili bilgi ve yetkinliğe sahip bir ekip oluşturulur. "
                "Ekip üyeleri sorumluluklarına göre atanır."
            ),
        },
        {
            "step": "D2",
            "title": "Problemin Tanımı",
            "detail": (
                "Problem açık, ölçülebilir ve objektif kriterlerle tanımlanır. "
                "Müşteri şikayeti, ürün adı, tarih, yer, miktar gibi detaylara "
                "yer verilir. 5N1K sorularıyla desteklenmesi önerilir."
            ),
        },
        {
            "step": "D3",
            "title": "Geçici Önlemler",
            "detail": (
                "Problemin müşteriyi ya da süreci daha fazla etkilemesini önlemek "
                "amacıyla geçici, hızlı çözümler uygulanır. Bu önlemlerin etkili "
                "olduğu doğrulanmalıdır."
            ),
        },
        {
            "step": "D4",
            "title": "Kök Neden Analizi",
            "detail": (
                "Problemin temel nedenleri araştırılır. Yüzeysel belirtiler değil, "
                "problemi gerçekten yaratan neden(ler) tespit edilir. '5 Neden' "
                "tekniği, balık kılçığı diyagramı gibi araçlar kullanılabilir."
            ),
        },
        {
            "step": "D5",
            "title": "Kalıcı Çözüm Geliştirme",
            "detail": (
                "Kök nedenlere yönelik kalıcı çözüm önerileri oluşturulur. Bu "
                "çözümlerin uygulanabilirliği, riskleri ve etkisi değerlendirilerek "
                "en uygun çözüm seçilir."
            ),
        },
        {
            "step": "D6",
            "title": "Kalıcı Çözümün Uygulanması",
            "detail": (
                "Seçilen kalıcı çözüm(ler) sahada uygulanır. Uygulama sonrası "
                "doğrulama yapılır, gerekiyorsa düzeltici aksiyonlar alınır. "
                "Etkinlik kontrolü bu aşamada önemlidir."
            ),
        },
        {
            "step": "D7",
            "title": "Önleyici Faaliyetler",
            "detail": (
                "Benzer problemlerin başka ürün, proses ya da alanlarda "
                "tekrarlanmaması için sistematik önleyici faaliyetler planlanır ve "
                "uygulanır. Proaktif kalite anlayışı burada devrededir."
            ),
        },
        {
            "step": "D8",
            "title": "Takdir ve Kapanış",
            "detail": (
                "Ekip üyeleri, çözüm sürecine katkılarından dolayı takdir edilir. "
                "Tüm dokümantasyon tamamlanır ve süreç resmi olarak kapatılır. "
                "Öğrenilen dersler paylaşılır."
            ),
        },
    ],
}


class GuideManager:
    """Manages guide steps and resources for quality-report methods."""

    def __init__(self) -> None:
        """Initialize the guide cache."""
        self._cache: Dict[str, Dict[str, Any]] = {}

    def load_guide(self, path: str) -> Dict[str, Any]:
        """Load guide information from the given path."""
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError as exc:
            raise GuideNotFoundError(path) from exc

    def get_format(self, method: str) -> Dict[str, Any]:
        """Return the guide dictionary for the given method."""
        if method not in self._cache:
            base_dir = Path(__file__).resolve().parents[1] / "Guidelines"
            guide_path = base_dir / f"{method}_Guide.json"
            try:
                self._cache[method] = self.load_guide(str(guide_path))
            except GuideNotFoundError:
                if method == "8D":
                    self._cache[method] = DEFAULT_8D_GUIDE
                else:
                    raise
        return self._cache[method]
