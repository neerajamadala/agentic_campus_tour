# agent.py
from tools import MapTool, CalendarTool, DirectoryTool

class MockAgent:
    def run(self, query):
        query_lower = query.lower()
        
        # Map queries
        if "directions" in query_lower or "how to get" in query_lower:
            return MapTool.func(query)
        
        # Calendar queries
        elif "event" in query_lower or "happening" in query_lower:
            return CalendarTool.func(query)
        
        # Directory queries
        elif any(k in query_lower for k in ["registrar", "library", "counseling"]):
            for key in ["Registrar", "Library", "Counseling"]:
                if key.lower() in query_lower:
                    return DirectoryTool.func(key)
        
        # Generic fallback
        fallback_answers = {
            "library": "Library is open 8AM to 10PM daily.",
            "register": "Register for courses via Registrar or the online portal.",
        }
        for key, ans in fallback_answers.items():
            if key in query_lower:
                return ans

        return "Sorry, I don't have that information yet."

agent = MockAgent()
