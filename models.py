"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str
import math


class NearEarthObject:
    """Đại diện cho một đối tượng gần Trái Đất (NEO).

    NEO bao gồm các thông số nhận dạng và vật lý như định danh chính, 
    tên IAU (tuỳ chọn), đường kính (có thể không xác định), và cờ đánh dấu 
    nếu đối tượng có khả năng nguy hiểm.
    """

    def __init__(self, designation: str, name: str = None, 
                 diameter: float = float('nan'), hazardous: bool = False):
        """Khởi tạo một `NearEarthObject` mới.

        :param designation: Định danh chính, là bắt buộc.
        :param name: Tên (tuỳ chọn).
        :param diameter: Đường kính (tuỳ chọn, mặc định là không xác định).
        :param hazardous: Đánh dấu nguy hiểm (mặc định là không nguy hiểm).
        """
        self.designation = designation
        self.name = name or None
        self.diameter = diameter
        self.hazardous = bool(hazardous)

        # Tạo danh sách rỗng ban đầu để lưu các lần tiếp cận gần.
        self.approaches = []

    @property
    def fullname(self):
        """Trả về tên đầy đủ của đối tượng NEO này."""
        return f"{self.designation} ({self.name})" if self.name else self.designation

    def __str__(self):
        """Trả về chuỗi biểu diễn dạng đọc được của đối tượng."""
        base_info = f"NEO {self.fullname}"
        size_info = f" với đường kính {self.diameter:.3f} km" if not math.isnan(self.diameter) else ""
        hazard_info = " là đối tượng nguy hiểm." if self.hazardous else " không nguy hiểm."
        return base_info + size_info + hazard_info

    def __repr__(self):
        """Trả về chuỗi biểu diễn dạng lập trình của đối tượng."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")


class CloseApproach:
    """Đại diện cho một lần tiếp cận gần của NEO với Trái Đất."""

    def __init__(self, designation: str, time: str = None, 
                 distance: float = 0.0, velocity: float = 0.0, neo=None):
        """Khởi tạo một `CloseApproach`.

        :param designation: Định danh chính của NEO liên quan.
        :param time: Thời điểm tiếp cận.
        :param distance: Khoảng cách gần nhất (AU).
        :param velocity: Tốc độ tiếp cận (km/s).
        :param neo: Đối tượng NEO liên quan (ban đầu là None).
        """
        self._designation = designation
        self.time = cd_to_datetime(time) if time else None
        self.distance = float(distance)
        self.velocity = float(velocity)
        self.neo = neo

    @property
    def time_str(self):
        """Trả về thời gian tiếp cận dưới dạng chuỗi định dạng."""
        return datetime_to_str(self.time) if self.time else "Unknown Time"

    def __str__(self):
        """Trả về chuỗi biểu diễn dạng đọc được của lần tiếp cận."""
        return (f"Vào {self.time_str}, '{self._designation}' tiếp cận Trái Đất "
                f"ở khoảng cách {self.distance:.2f} AU với tốc độ {self.velocity:.2f} km/s.")

    def __repr__(self):
        """Trả về chuỗi biểu diễn dạng lập trình của lần tiếp cận."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")