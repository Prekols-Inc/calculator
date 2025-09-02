import { useState } from 'react'
import Display from './Display'
import Button from './Button'
import './Calculator.css'

const Calculator = () => {
    const [currentOperand, setCurrentOperand] = useState('0')
    const [previousOperand, setPreviousOperand] = useState('')
    const [operation, setOperation] = useState(null)
    const [resetScreen, setResetScreen] = useState(false)

    const appendNumber = (number) => {
        if (currentOperand === '0' || resetScreen) {
            setCurrentOperand(number.toString())
            setResetScreen(false)
        } else {
            if (number === '.' && currentOperand.includes('.')) return
            setCurrentOperand(currentOperand + number.toString())
        }
    }

    const chooseOperation = (op) => {
        if (currentOperand === '0') return

        if (previousOperand !== '') {
            compute()
        }

        setOperation(op)
        setPreviousOperand(`${currentOperand} ${op}`)
        setResetScreen(true)
    }

    const compute = () => {
        let computation
        const prev = parseFloat(previousOperand)
        const current = parseFloat(currentOperand)

        if (isNaN(prev) || isNaN(current)) return

        switch (operation) {
            case '+':
                computation = prev + current
                break
            case '-':
                computation = prev - current
                break
            case '*':
                computation = prev * current
                break
            case '÷':
                computation = prev / current
                break
            default:
                return
        }

        setCurrentOperand(computation.toString())
        setOperation(null)
        setPreviousOperand('')
        setResetScreen(true)
    }

    const clear = () => {
        setCurrentOperand('0')
        setPreviousOperand('')
        setOperation(null)
    }

    const deleteNumber = () => {
        if (currentOperand.length === 1) {
            setCurrentOperand('0')
        } else {
            setCurrentOperand(currentOperand.slice(0, -1))
        }
    }

    return (
        <div className="calculator-container">
            <Display
                currentOperand={currentOperand}
                previousOperand={previousOperand}
            />
            <div className="buttons-grid">
                <Button className="clear" onClick={clear}>AC</Button>
                <Button onClick={deleteNumber}>DEL</Button>
                <Button className="operation" onClick={() => chooseOperation('÷')}>÷</Button>
                <Button className="operation" onClick={() => chooseOperation('*')}>×</Button>

                <Button onClick={() => appendNumber(7)}>7</Button>
                <Button onClick={() => appendNumber(8)}>8</Button>
                <Button onClick={() => appendNumber(9)}>9</Button>
                <Button className="operation" onClick={() => chooseOperation('-')}>-</Button>

                <Button onClick={() => appendNumber(4)}>4</Button>
                <Button onClick={() => appendNumber(5)}>5</Button>
                <Button onClick={() => appendNumber(6)}>6</Button>
                <Button className="operation" onClick={() => chooseOperation('+')}>+</Button>

                <Button onClick={() => appendNumber(1)}>1</Button>
                <Button onClick={() => appendNumber(2)}>2</Button>
                <Button onClick={() => appendNumber(3)}>3</Button>

                <Button className="equals" onClick={compute}>=</Button>

                <Button onClick={() => appendNumber(0)}>0</Button>
                <Button onClick={() => appendNumber('.')}>.</Button>
            </div>
        </div>
    )
}

export default Calculator
