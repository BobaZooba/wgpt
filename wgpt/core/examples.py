# Copyright 2023 Boris Zubarev. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

EXAMPLES = [
    """Input: The skies are clear with a temperature of about 25 degrees. The wind is blowing gently at around 7kph. Visibility is high and the air is quite dry with a humidity around 30%. There's no precipitation. Feels like it's exactly 25 degrees. The air quality is very good today.
Output: {"weather": "clear", "temperature": 25, "wind_speed": 7.0, "humidity": 30.0, "precipitation": "none", "visibility": "high", "air_quality": "good", "real_feel_temperature": 25}""",
    """Input: It's snowing outside and the temperature is -5 degrees. There's a strong wind blowing at 25kph. Visibility is very low because of the snow. Humidity is around 80%. Air quality is moderate today. The real feel is much lower at -10 degrees due to wind chill.
Output: {"weather": "snow", "temperature": -5, "wind_speed": 25.0, "humidity": 80.0, "precipitation": "snow", "visibility": "low", "air_quality": "moderate", "real_feel_temperature": -10}""",
    """Input: Expect a cloudy evening with a temperature of about 18 degrees. There is a slight chance of light showers, and the wind is gentle at 5 km/h.
Output: {"weather": "cloudy", "temperature": 18, "wind_speed": 5.0, "humidity": null, "precipitation": "light", "visibility": "good", "air_quality": null, "real_feel_temperature": null}""",
    """Input: The weather forecast is predicting foggy conditions in the morning, with visibility being quite low. The temperature is expected to be around 10 degrees.
Output: {"weather": "foggy", "temperature": 10, "wind_speed": null, "humidity": null, "precipitation": "none", "visibility": "low", "air_quality": null, "real_feel_temperature": null}""",
    """Input: There's a scorching heatwave, and the blistering temperature hits 35 degrees. Winds are breezy, providing slight relief.
Output: {"weather": "sunny", "temperature": 35, "wind_speed": null, "humidity": null, "precipitation": "none", "visibility": "good", "air_quality": null, "real_feel_temperature": 35}""",
    """Input: It's a perfect summer's day with clear skies and a temperature of 28 degrees. There's a light breeze at 8 kph. No clouds in sight means maximum visibility. It's quite dry with a humidity of around 35%. No precipitation is expected. The air feels good and it actually feels like 28 degrees.
Output: {"weather": "clear", "temperature": 28, "wind_speed": 8.0, "humidity": 35.0, "precipitation": "none", "visibility": "high", "air_quality": "good", "real_feel_temperature": 28}""",
    """Input: It's heavily snowing with temperature dropping down to -8 degrees, accompanied by strong gusts of wind at 28 kph. Visibility is extremely poor due to the snowfall, and there's a relative humidity of 86%. The quality of air is a bit poor due to continuous snowing. Despite the stated temperature, wind chill makes it feel like -14 degrees.
Output: {"weather": "snow", "temperature": -8, "wind_speed": 28.0, "humidity": 86.0, "precipitation": "heavy", "visibility": "poor", "air_quality": "poor", "real_feel_temperature": -14}""",
    """Input: Clouds are covering the entire sky blocking the sun, with the temperatures around 20 degrees. A light drizzle is expected later in the day. The wind is mild at 4 km/h, and visibility is high. Humidity levels are unknown, as is the air quality.
Output: {"weather": "cloudy", "temperature": 20, "wind_speed": 4.0, "humidity": null, "precipitation": "drizzle", "visibility": "high", "air_quality": null, "real_feel_temperature": null}""",
    """Input: We are experiencing a rather foggy morning today with temperatures hovering around 15 degrees. The wind speed is not significant. Visibility is severely impaired due to fog. Precipitation, humidity details, air quality as well as real feel temperature aren't available at the moment.
Output: {"weather": "foggy", "temperature": 15, "wind_speed": null, "humidity": null, "precipitation": "none", "visibility": "low", "air_quality": null, "real_feel_temperature": null}""",
    """Input: It's a typical hot day in the desert with the temperature currently at 40 degrees. The wind speed is unknown. The humidity is low at 10%. No precipitation is expected. Visibility is good and the air quality is poor. It feels like 45 degrees because of the heat.
Output: {"weather": "sunny", "temperature": 40, "wind_speed": null, "humidity": 10.0, "precipitation": "none", "visibility": "high", "air_quality": "poor", "real_feel_temperature": 45}""",
    """Input: The weather is a bit cool with a temperature of 12 degrees. The wind is blowing at a pleasant speed of 11 kilometers per hour. No precipitation today means the visibility is high. The humidity is 55% and the air quality is very good. However, the real feel temperature is around 10 degrees.
Output: {"weather": "cool", "temperature": 12, "wind_speed": 11.0, "humidity": 55.0, "precipitation": "none", "visibility": "high", "air_quality": "good", "real_feel_temperature": 10}""",
    """Input: Today, it is lightly raining with temperatures around 18 degrees. The wind speed is approximately 9 kilometers per hour. Visibility is average due to the rain and the humidity is at 70%. Good news is that the air quality is fairly good today. It feels a little cooler than the actual temperature, roughly around 16 degrees.
Output: {"weather": "rain", "temperature": 18, "wind_speed": 9.0, "humidity": 70.0, "precipitation": "light", "visibility": "medium", "air_quality": "good", "real_feel_temperature": 16}""",
    """Input: A warm sunny day awaits with temperatures rising to a comfortable 23 degrees. Winds are moving at a slower pace with speeds around 5 km/h. The sky is free of clouds, promising great visibility and low humidity of 20%.  The quality of air is excellent and the temperature is as it feels.
Output: {"weather": "sunny", "temperature": 23, "wind_speed": 5.0, "humidity": 20.0, "precipitation": "none", "visibility": "high", "air_quality": "excellent", "real_feel_temperature": 23}""",
    """Input: With moderate showers, it's quite chilly today at 5 degrees. The wind is pretty strong, blowing at 21 km/h. Naturally, the visibility is poor due to the rain showers. The air is wet with a high humidity of around 90%. Air quality is fair, and the temperature definitely feels colder at 0 degrees.
Output: {"weather": "rain", "temperature": 5, "wind_speed": 21.0, "humidity": 90.0, "precipitation": "moderate", "visibility": "low", "air_quality": "fair", "real_feel_temperature": 0}""",
    """Input: We're currently seeing cloudy skies with temperatures around 16 degrees. There is a gentle wind blowing at around 7 km/h, with no signs of rain. Visibility is good and humidity is about 45%. There's no definitive data on air quality and real feel temperature at present.
Output: {"weather": "cloudy", "temperature": 16, "wind_speed": 7.0, "humidity": 45.0, "precipitation": "none", "visibility": "good", "air_quality": null, "real_feel_temperature": null}""",
]
