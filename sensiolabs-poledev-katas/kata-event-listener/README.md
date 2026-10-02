# Kata 2: Event Listener / Event Dispatcher

Source: https://github.com/devdrops/Katas/tree/kata-event-listener

## Problem

Implement an event dispatcher system (Observer pattern) for decoupled communication between components.

## Goals

- Register listeners for events
- Dispatch events to all listeners
- Support priority/ordering
- Allow listener removal
- Event object with metadata

## Features

1. **Event classes**: typed events with payload
2. **Listener registration**: callable, closure, invokable object
3. **Priority system**: high priority listeners fire first
4. **Stop propagation**: listener can halt further processing
5. **Lazy listeners**: instantiated only when event fires
6. **Wildcard listeners**: listen to event patterns

## Examples

```python
# Event dispatcher
dispatcher = EventDispatcher()
dispatcher.subscribe("user.created", lambda e: print(f"Welcome {e.data['name']}"))
dispatcher.dispatch("user.created", {"name": "Alice"})
# => "Welcome Alice"
```

## Exercises

1. Basic dispatcher with string event names
2. Typed event objects
3. Priority ordering
4. Stop propagation
5. Subscriber interface (auto-register methods)
6. Event store/history for debugging
7. Async event processing
8. Testing: spy on dispatched events