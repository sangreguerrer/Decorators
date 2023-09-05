import types
import datetime
import os
def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            name = old_function.__name__
            time = datetime.datetime.now()
            args=args
            kwargs=kwargs
            result = old_function(*args, **kwargs)
            with open(path,"a",encoding='utf=8') as file:
                file.write(f'''
                               name:{name},
                               time:{time},
                               args:{args}
                               kwargs:{kwargs}
                               result:{result}
                           ''')
            return result
        return new_function
    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')
    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def flat_generator(list_of_lists):
            for sub in list_of_lists:
                for new_sub in sub:
                    yield new_sub
        list_of_lists_1 = [
            ['a', 'b', 'c'],
            ['d', 'e', 'f', 'h', False],
            [1, 2, None]
            ]

        for flat_iterator_item, check_item in zip(
                flat_generator(list_of_lists_1),
                ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
        ):

            assert flat_iterator_item == check_item

        assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

        assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


if __name__ == '__main__':
    test_2()
