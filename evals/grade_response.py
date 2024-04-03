import json
import sys


def safe_input(text):
    verdict = {'y': True, 'n': False}

    ans = input(text)
    while ans not in ['y', 'n']:
        ans = input(text)

    return verdict[ans]


def main():
    with open(sys.argv[1]) as f:
        results = json.load(f)


    for result in results:
        if result['good_retv'] is not None:
            continue
        print(
            f'Question: {result["query"]}',
            f'Document: {result["target_document"]}',
            f'Answer: {result["answer"]}',
            f'Response: {result["response"]}',
            sep='\n'
        )
        try:
            result.update({
                'good_retv': safe_input('Good retrieval (y/n)? '),
                'refuse': safe_input('Refused (y/n)?'),
                'good_resp': safe_input('Good response (y/n)? '),
                'comment': input('Comment: ')
            })
        except KeyboardInterrupt:
            break
        print('='*30)

    with open(sys.argv[1], 'w') as f:
        json.dump(results, f, indent=2)


    def count_condition(condition):
        freq = 0
        for result in results:
            if condition(result):
                freq += 1
        return freq


    n_q = len(results)
    print(f'Model: {sys.argv[1]}')

    corr_retv = count_condition(lambda r: r['good_retv'])
    print(f'Retrievals (Correct / Incorrect): {corr_retv} / {n_q - corr_retv}')

    corr_retv_ans = count_condition(lambda r: r['good_retv'] and (r['good_resp'] or r['refuse']))
    corr_retv_refuse = count_condition(lambda r: r['good_retv'] and r['refuse'])
    print(f'Good Answer w/ correct retrievals: {corr_retv_ans} ({corr_retv_refuse} refusals)')

    incor_retv_ans = count_condition(lambda r: (not r['good_retv']) and (r['good_resp'] or r['refuse']))
    incor_retv_refuse = count_condition(lambda r: (not r['good_retv']) and r['refuse'])
    print(f'Good Answer w/ incorrect retrievals: {incor_retv_ans} ({incor_retv_refuse} refusals)')

    good_ans = count_condition(lambda r: r['good_resp'] or r['refuse'])
    print(f'Total good answers: {good_ans} / {n_q}')


if __name__ == '__main__':
    main()
