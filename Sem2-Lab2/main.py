import requests
import pandas as pd
import yaml
from abc import ABC, abstractmethod

class Component(ABC):
    """
    Базовый интерфейс Компонента определяет поведение, которое изменяется
    декораторами.
    """
    @abstractmethod
    def operation(self):
        pass

class Decorator(Component):
    """
    Базовый класс Декоратора следует тому же интерфейсу, что и другие
    компоненты. Основная цель этого класса - определить интерфейс обёртки для
    всех конкретных декораторов. Реализация кода обёртки по умолчанию может
    включать в себя поле для хранения завёрнутого компонента и средства его
    инициализации.
    """

    _component: Component = None

    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self):
        return self._component

    def operation(self):
        return self._component.operation()

class FetchCourses(Component):
    """
    Конкретный компонент, реализующий получение всех курсов валют
    с помощью API Центробанка
    """

    def __init__(self, courses: list[str] | None = None) -> None:
        super().__init__()

        self._courses = courses

    def operation(self) -> dict:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        if response.status_code != 200:
            raise Exception("Ошибка выполнения запроса к API")
        try:
            data = response.json()
        except ValueError:
            raise Exception("Ошибка выполнения запроса к API")

        valutes = data['Valute']
        result: list[dict] = []

        for v in valutes:
            result.append(valutes[v])

        if self._courses is not None:
            return list(filter(lambda x: x['CharCode'] in self._courses, result))
        else:
            return result
            
class ConvertToYAML(Decorator):
    """
    Конкретный декоратор, трансформирующий результат в формат YAML
    """
    def operation(self) -> str:
        return yaml.safe_dump(self.component.operation(), allow_unicode=True)

class ConvertToCSV(Decorator):
    """
    Конкретный декоратор, трансформирующий результат в формат CSV
    """
    def operation(self) -> str:
        df = pd.DataFrame(self.component.operation())
        return df.to_csv(index=False)

if __name__ == "__main__":
    component = FetchCourses(['USD'])
    print("Результат:")
    print(component.operation())
    print("Результат, преобразованный в YAML:")
    print(ConvertToYAML(component).operation())
    print("Результат, преобразованный в CSV:")
    print(ConvertToCSV(component).operation())
