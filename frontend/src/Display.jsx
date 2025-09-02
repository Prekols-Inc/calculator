const Display = ({ currentOperand, previousOperand }) => {
    return (
        <div className="display">
            <div className="previous-operand">{previousOperand}</div>
            <div className="current-operand">{currentOperand}</div>
        </div>
    )
}

export default Display
