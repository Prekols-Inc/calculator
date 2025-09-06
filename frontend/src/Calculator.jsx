import React, { useState } from "react";
import "./styles/Calculator.css";
import { calculate } from "./API";

const error_msg = "Error";

export default function Calculator() {
    const [expression, setExpression] = useState("");

    const buttons = [
        "7", "8", "9", "/",
        "4", "5", "6", "*",
        "1", "2", "3", "-",
        "0", "(", ")",
        "+", ".", "=", "C"
    ];

    const handleClick = (value) => {
        if (value === "C") {
            setExpression("");
        } else if (value === "=") {
            calculate(expression)
                .then((result) => {
                    setExpression(String(result));
                })
                .catch(() => {
                    setExpression(error_msg);
                });
        } else {
            if (expression === error_msg) {
                setExpression(value);
            } else {
                setExpression(expression + value);
            }
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
