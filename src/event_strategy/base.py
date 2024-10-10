from abc import ABC, abstractmethod
from typing import List, Dict

from schemas.event_schemas import EventIntent


class RoutingStrategy(ABC):
    strategies = {}

    def __init_subclass__(cls, strategy_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if strategy_name:
            cls.strategies[strategy_name] = cls

    @abstractmethod
    def filter_intents(self, routing_intents: List[EventIntent]) -> List[EventIntent]:
        pass


class AllStrategy(RoutingStrategy, strategy_name="ALL"):
    def filter_intents(self, routing_intents: List[EventIntent]) -> List[EventIntent]:
        return routing_intents


class ImportantStrategy(RoutingStrategy, strategy_name="IMPORTANT"):
    def filter_intents(self, routing_intents: List[EventIntent]) -> List[EventIntent]:
        return [intent for intent in routing_intents if intent.important == True]


class SmallStrategy(RoutingStrategy, strategy_name="SMALL"):
    def filter_intents(self, routing_intents: List[EventIntent]) -> List[EventIntent]:
        return [intent for intent in routing_intents if intent.get("bytes", 0) < 1024]


class CustomStrategy(RoutingStrategy, strategy_name="CUSTOM"):
    def __init__(self, custom_function: str):
        self.custom_function = custom_function

    def filter_intents(self, routing_intents) -> List[EventIntent]:
        routing_intents = [i.dict() for i in routing_intents]
        try:
            custom_func = eval(self.custom_function)
            if callable(custom_func):
                result = custom_func(routing_intents)
                return [EventIntent.from_orm(intent) for intent in result]
            else:
                raise ValueError("Strategia must be callable (func)")
        except Exception as e:
            raise ValueError(f"Custom strategia error {str(e)}")
