import React, { useState } from "react";
import "./Calculator.css";

export default function Calculator() {
    const [expression, setExpression] = useState("");

    const buttons = [
        "7", "8", "9", "/",
        "4", "5", "6", "*",
        "1", "2", "3", "-",
        "0", ".", "+",
        "(", ")", "=", "C"
    ];

    const handleClick = (value) => {
        if (value === "C") {
            setExpression("");
        } else if (value === "=") {
            try {
                const result = eval(expression);
                setExpression(String(result));
            } catch {
                setExpression("Ошибка");
            }
        } else {
            setExpression(expression + value);
        }
    };

    return (
        <div className="calculator">
            <div className="calc-wrapper">
                <div className="display">{expression || "0"}</div>
                <div className="buttons">
                    {buttons.map((btn) => (
                        <button
                            key={btn}
                            onClick={() => handleClick(btn)}
                            className={
                                btn === "=" ? "equal" : btn === "C" ? "clear" :
                                    ["/", "*", "-", "+"].includes(btn) ? "operator" : ""
                            }
                        >
                            {btn}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}
